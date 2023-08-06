Object.defineProperty(exports, "__esModule", { value: true });
exports.escapeFilterValue = exports.tokenizeSearch = exports.QueryResults = exports.TokenType = void 0;
var tslib_1 = require("tslib");
var utils_1 = require("app/utils");
var TokenType;
(function (TokenType) {
    TokenType[TokenType["OPERATOR"] = 0] = "OPERATOR";
    TokenType[TokenType["FILTER"] = 1] = "FILTER";
    TokenType[TokenType["FREE_TEXT"] = 2] = "FREE_TEXT";
})(TokenType = exports.TokenType || (exports.TokenType = {}));
function isOp(t) {
    return t.type === TokenType.OPERATOR;
}
function isBooleanOp(value) {
    return ['OR', 'AND'].includes(value.toUpperCase());
}
function isParen(token, character) {
    return (token !== undefined &&
        isOp(token) &&
        ['(', ')'].includes(token.value) &&
        token.value === character);
}
// TODO(epurkhiser): This is legacy from before the existence of
// searchSyntax/parser. We should absolutely replace the internals of this API
// with `parseSearch`.
var QueryResults = /** @class */ (function () {
    function QueryResults(strTokens) {
        var e_1, _a;
        var _this = this;
        this.tokens = [];
        try {
            for (var strTokens_1 = tslib_1.__values(strTokens), strTokens_1_1 = strTokens_1.next(); !strTokens_1_1.done; strTokens_1_1 = strTokens_1.next()) {
                var token = strTokens_1_1.value;
                var tokenState = TokenType.FREE_TEXT;
                if (isBooleanOp(token)) {
                    this.addOp(token.toUpperCase());
                    continue;
                }
                if (token.startsWith('(')) {
                    var parenMatch = token.match(/^\(+/g);
                    if (parenMatch) {
                        parenMatch[0].split('').map(function (paren) { return _this.addOp(paren); });
                        token = token.replace(/^\(+/g, '');
                    }
                }
                // Traverse the token and check if it's a filter condition or free text
                for (var i = 0, len = token.length; i < len; i++) {
                    var char = token[i];
                    if (i === 0 && (char === '"' || char === ':')) {
                        break;
                    }
                    // We may have entered a filter condition
                    if (char === ':') {
                        var nextChar = token[i + 1] || '';
                        if ([':', ' '].includes(nextChar)) {
                            tokenState = TokenType.FREE_TEXT;
                        }
                        else {
                            tokenState = TokenType.FILTER;
                        }
                        break;
                    }
                }
                var trailingParen = '';
                if (token.endsWith(')') && !token.includes('(')) {
                    var parenMatch = token.match(/\)+$/g);
                    if (parenMatch) {
                        trailingParen = parenMatch[0];
                        token = token.replace(/\)+$/g, '');
                    }
                }
                if (tokenState === TokenType.FREE_TEXT && token.length) {
                    this.addFreeText(token);
                }
                else if (tokenState === TokenType.FILTER) {
                    this.addStringFilter(token, false);
                }
                if (trailingParen !== '') {
                    trailingParen.split('').map(function (paren) { return _this.addOp(paren); });
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (strTokens_1_1 && !strTokens_1_1.done && (_a = strTokens_1.return)) _a.call(strTokens_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
    }
    QueryResults.prototype.formatString = function () {
        var e_2, _a;
        var formattedTokens = [];
        try {
            for (var _b = tslib_1.__values(this.tokens), _c = _b.next(); !_c.done; _c = _b.next()) {
                var token = _c.value;
                switch (token.type) {
                    case TokenType.FILTER:
                        if (token.value === '' || token.value === null) {
                            formattedTokens.push(token.key + ":\"\"");
                        }
                        else if (/[\s\(\)\\"]/g.test(token.value)) {
                            formattedTokens.push(token.key + ":\"" + utils_1.escapeDoubleQuotes(token.value) + "\"");
                        }
                        else {
                            formattedTokens.push(token.key + ":" + token.value);
                        }
                        break;
                    case TokenType.FREE_TEXT:
                        if (/[\s\(\)\\"]/g.test(token.value)) {
                            formattedTokens.push("\"" + utils_1.escapeDoubleQuotes(token.value) + "\"");
                        }
                        else {
                            formattedTokens.push(token.value);
                        }
                        break;
                    default:
                        formattedTokens.push(token.value);
                }
            }
        }
        catch (e_2_1) { e_2 = { error: e_2_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_2) throw e_2.error; }
        }
        return formattedTokens.join(' ').trim();
    };
    QueryResults.prototype.addStringFilter = function (filter, shouldEscape) {
        if (shouldEscape === void 0) { shouldEscape = true; }
        var _a = tslib_1.__read(parseFilter(filter), 2), key = _a[0], value = _a[1];
        this.addFilterValues(key, [value], shouldEscape);
        return this;
    };
    QueryResults.prototype.addFilterValues = function (key, values, shouldEscape) {
        var e_3, _a;
        if (shouldEscape === void 0) { shouldEscape = true; }
        try {
            for (var values_1 = tslib_1.__values(values), values_1_1 = values_1.next(); !values_1_1.done; values_1_1 = values_1.next()) {
                var value = values_1_1.value;
                // Filter values that we insert through the UI can contain special characters
                // that need to escaped. User entered filters should not be escaped.
                var escaped = shouldEscape ? escapeFilterValue(value) : value;
                var token = { type: TokenType.FILTER, key: key, value: escaped };
                this.tokens.push(token);
            }
        }
        catch (e_3_1) { e_3 = { error: e_3_1 }; }
        finally {
            try {
                if (values_1_1 && !values_1_1.done && (_a = values_1.return)) _a.call(values_1);
            }
            finally { if (e_3) throw e_3.error; }
        }
        return this;
    };
    QueryResults.prototype.setFilterValues = function (key, values, shouldEscape) {
        if (shouldEscape === void 0) { shouldEscape = true; }
        this.removeFilter(key);
        this.addFilterValues(key, values, shouldEscape);
        return this;
    };
    Object.defineProperty(QueryResults.prototype, "filters", {
        get: function () {
            var reducer = function (acc, token) {
                var _a;
                var _b;
                return (tslib_1.__assign(tslib_1.__assign({}, acc), (_a = {}, _a[token.key] = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(((_b = acc[token.key]) !== null && _b !== void 0 ? _b : []))), [token.value]), _a)));
            };
            return this.tokens
                .filter(function (t) { return t.type === TokenType.FILTER; })
                .reduce(reducer, {});
        },
        enumerable: false,
        configurable: true
    });
    QueryResults.prototype.getFilterValues = function (key) {
        var _a;
        return (_a = this.filters[key]) !== null && _a !== void 0 ? _a : [];
    };
    QueryResults.prototype.getFilterKeys = function () {
        return Object.keys(this.filters);
    };
    QueryResults.prototype.hasFilter = function (key) {
        return this.getFilterValues(key).length > 0;
    };
    QueryResults.prototype.removeFilter = function (key) {
        this.tokens = this.tokens.filter(function (token) { return token.key !== key; });
        // Now the really complicated part: removing parens that only have one element in them.
        // Since parens are themselves tokens, this gets tricky. In summary, loop through the
        // tokens until we find the innermost open paren. Then forward search through the rest of the tokens
        // to see if that open paren corresponds to a closed paren with one or fewer items inside.
        // If it does, delete those parens, and loop again until there are no more parens to delete.
        var parensToDelete = [];
        var cleanParens = function (_, idx) { return !parensToDelete.includes(idx); };
        do {
            if (parensToDelete.length) {
                this.tokens = this.tokens.filter(cleanParens);
            }
            parensToDelete = [];
            for (var i = 0; i < this.tokens.length; i++) {
                var token = this.tokens[i];
                if (!isOp(token) || token.value !== '(') {
                    continue;
                }
                var alreadySeen = false;
                for (var j = i + 1; j < this.tokens.length; j++) {
                    var nextToken = this.tokens[j];
                    if (isOp(nextToken) && nextToken.value === '(') {
                        // Continue down to the nested parens. We can skip i forward since we know
                        // everything between i and j is NOT an open paren.
                        i = j - 1;
                        break;
                    }
                    else if (!isOp(nextToken)) {
                        if (alreadySeen) {
                            // This has more than one term, no need to delete
                            break;
                        }
                        alreadySeen = true;
                    }
                    else if (isOp(nextToken) && nextToken.value === ')') {
                        // We found another paren with zero or one terms inside. Delete the pair.
                        parensToDelete = [i, j];
                        break;
                    }
                }
                if (parensToDelete.length > 0) {
                    break;
                }
            }
        } while (parensToDelete.length > 0);
        // Now that all erroneous parens are removed we need to remove dangling OR/AND operators.
        // I originally removed all the dangling properties in a single loop, but that meant that
        // cases like `a OR OR b` would remove both operators, when only one should be removed. So
        // instead, we loop until we find an operator to remove, then go back to the start and loop
        // again.
        var toRemove = -1;
        do {
            if (toRemove >= 0) {
                this.tokens.splice(toRemove, 1);
                toRemove = -1;
            }
            for (var i = 0; i < this.tokens.length; i++) {
                var token = this.tokens[i];
                var prev = this.tokens[i - 1];
                var next = this.tokens[i + 1];
                if (isOp(token) && isBooleanOp(token.value)) {
                    if (prev === undefined || isOp(prev) || next === undefined || isOp(next)) {
                        // Want to avoid removing `(term) OR (term)`
                        if (isParen(prev, ')') && isParen(next, '(')) {
                            continue;
                        }
                        toRemove = i;
                        break;
                    }
                }
            }
        } while (toRemove >= 0);
        return this;
    };
    QueryResults.prototype.removeFilterValue = function (key, value) {
        var values = this.getFilterValues(key);
        if (Array.isArray(values) && values.length) {
            this.setFilterValues(key, values.filter(function (item) { return item !== value; }));
        }
    };
    QueryResults.prototype.addFreeText = function (value) {
        var token = { type: TokenType.FREE_TEXT, value: formatQuery(value) };
        this.tokens.push(token);
        return this;
    };
    QueryResults.prototype.addOp = function (value) {
        var token = { type: TokenType.OPERATOR, value: value };
        this.tokens.push(token);
        return this;
    };
    Object.defineProperty(QueryResults.prototype, "freeText", {
        get: function () {
            return this.tokens.filter(function (t) { return t.type === TokenType.FREE_TEXT; }).map(function (t) { return t.value; });
        },
        set: function (values) {
            var e_4, _a;
            this.tokens = this.tokens.filter(function (t) { return t.type !== TokenType.FREE_TEXT; });
            try {
                for (var values_2 = tslib_1.__values(values), values_2_1 = values_2.next(); !values_2_1.done; values_2_1 = values_2.next()) {
                    var v = values_2_1.value;
                    this.addFreeText(v);
                }
            }
            catch (e_4_1) { e_4 = { error: e_4_1 }; }
            finally {
                try {
                    if (values_2_1 && !values_2_1.done && (_a = values_2.return)) _a.call(values_2);
                }
                finally { if (e_4) throw e_4.error; }
            }
        },
        enumerable: false,
        configurable: true
    });
    QueryResults.prototype.copy = function () {
        var q = new QueryResults([]);
        q.tokens = tslib_1.__spreadArray([], tslib_1.__read(this.tokens));
        return q;
    };
    QueryResults.prototype.isEmpty = function () {
        return this.tokens.length === 0;
    };
    return QueryResults;
}());
exports.QueryResults = QueryResults;
/**
 * Tokenize a search into a QueryResult
 *
 * Should stay in sync with src.sentry.search.utils:tokenize_query
 */
function tokenizeSearch(query) {
    var tokens = splitSearchIntoTokens(query);
    return new QueryResults(tokens);
}
exports.tokenizeSearch = tokenizeSearch;
/**
 * Splits search strings into tokens for parsing by tokenizeSearch.
 *
 * Should stay in sync with src.sentry.search.utils:split_query_into_tokens
 */
function splitSearchIntoTokens(query) {
    var queryChars = Array.from(query);
    var tokens = [];
    var token = '';
    var endOfPrevWord = '';
    var quoteType = '';
    var quoteEnclosed = false;
    for (var idx = 0; idx < queryChars.length; idx++) {
        var char = queryChars[idx];
        var nextChar = queryChars.length - 1 > idx ? queryChars[idx + 1] : null;
        token += char;
        if (nextChar !== null && !isSpace(char) && isSpace(nextChar)) {
            endOfPrevWord = char;
        }
        if (isSpace(char) && !quoteEnclosed && endOfPrevWord !== ':' && !isSpace(token)) {
            tokens.push(token.trim());
            token = '';
        }
        if (["'", '"'].includes(char) && (!quoteEnclosed || quoteType === char)) {
            quoteEnclosed = !quoteEnclosed;
            if (quoteEnclosed) {
                quoteType = char;
            }
        }
        if (quoteEnclosed && char === '\\' && nextChar === quoteType) {
            token += nextChar;
            idx++;
        }
    }
    var trimmedToken = token.trim();
    if (trimmedToken !== '') {
        tokens.push(trimmedToken);
    }
    return tokens;
}
/**
 * Checks if the string is only spaces
 */
function isSpace(s) {
    return s.trim() === '';
}
/**
 * Splits a filter on ':' and removes enclosing quotes if present, and returns
 * both sides of the split as strings.
 */
function parseFilter(filter) {
    var idx = filter.indexOf(':');
    var key = removeSurroundingQuotes(filter.slice(0, idx));
    var value = removeSurroundingQuotes(filter.slice(idx + 1));
    return [key, value];
}
function removeSurroundingQuotes(text) {
    var length = text.length;
    if (length <= 1) {
        return text;
    }
    var left = 0;
    for (; left <= length / 2; left++) {
        if (text.charAt(left) !== '"') {
            break;
        }
    }
    var right = length - 1;
    for (; right >= length / 2; right--) {
        if (text.charAt(right) !== '"' || text.charAt(right - 1) === '\\') {
            break;
        }
    }
    return text.slice(left, right + 1);
}
/**
 * Strips enclosing quotes and parens from a query, if present.
 */
function formatQuery(query) {
    return query.replace(/^["\(]+|["\)]+$/g, '');
}
/**
 * Some characters have special meaning in a filter value. So when they are
 * directly added as a value, we have to escape them to mean the literal.
 */
function escapeFilterValue(value) {
    // TODO(txiao): The types here are definitely wrong.
    // Need to dig deeper to see where exactly it's wrong.
    //
    // astericks (*) is used for wildcard searches
    return typeof value === 'string' ? value.replace(/([\*])/g, '\\$1') : value;
}
exports.escapeFilterValue = escapeFilterValue;
//# sourceMappingURL=tokenizeSearch.jsx.map