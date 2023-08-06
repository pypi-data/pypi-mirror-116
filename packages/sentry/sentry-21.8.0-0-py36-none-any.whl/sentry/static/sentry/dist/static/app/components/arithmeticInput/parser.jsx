Object.defineProperty(exports, "__esModule", { value: true });
exports.parseArithmetic = exports.TokenConverter = exports.Operation = void 0;
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var grammar_pegjs_1 = tslib_1.__importDefault(require("./grammar.pegjs"));
// This constant should stay in sync with the backend parser
var MAX_OPERATORS = 10;
var MAX_OPERATOR_MESSAGE = locale_1.t('Maximum operators exceeded');
var Operation = /** @class */ (function () {
    function Operation(_a) {
        var operator = _a.operator, _b = _a.lhs, lhs = _b === void 0 ? null : _b, rhs = _a.rhs;
        this.operator = operator;
        this.lhs = lhs;
        this.rhs = rhs;
    }
    return Operation;
}());
exports.Operation = Operation;
var Term = /** @class */ (function () {
    function Term(_a) {
        var term = _a.term, location = _a.location;
        this.term = term;
        this.location = location;
    }
    return Term;
}());
var TokenConverter = /** @class */ (function () {
    function TokenConverter() {
        var _this = this;
        this.tokenTerm = function (maybeFactor, remainingAdds) {
            if (remainingAdds.length > 0) {
                remainingAdds[0].lhs = maybeFactor;
                return flatten(remainingAdds);
            }
            else {
                return maybeFactor;
            }
        };
        this.tokenOperation = function (operator, rhs) {
            _this.numOperations += 1;
            if (_this.numOperations > MAX_OPERATORS &&
                !_this.errors.includes(MAX_OPERATOR_MESSAGE)) {
                _this.errors.push(MAX_OPERATOR_MESSAGE);
            }
            if (operator === 'divide' && rhs === '0') {
                _this.errors.push(locale_1.t('Division by 0 is not allowed'));
            }
            return new Operation({ operator: operator, rhs: rhs });
        };
        this.tokenFactor = function (primary, remaining) {
            remaining[0].lhs = primary;
            return flatten(remaining);
        };
        this.tokenField = function (term, location) {
            var field = new Term({ term: term, location: location });
            _this.fields.push(field);
            return term;
        };
        this.tokenFunction = function (term, location) {
            var func = new Term({ term: term, location: location });
            _this.functions.push(func);
            return term;
        };
        this.numOperations = 0;
        this.errors = [];
        this.fields = [];
        this.functions = [];
    }
    return TokenConverter;
}());
exports.TokenConverter = TokenConverter;
// Assumes an array with at least one element
function flatten(remaining) {
    var term = remaining.shift();
    while (remaining.length > 0) {
        var nextTerm = remaining.shift();
        if (nextTerm && term && nextTerm.lhs === null) {
            nextTerm.lhs = term;
        }
        term = nextTerm;
    }
    // Shouldn't happen, tokenTerm checks remaining and tokenFactor should have at least 1 item
    // This is just to help ts out
    if (term === undefined) {
        throw new Error('Unable to parse arithmetic');
    }
    return term;
}
function parseArithmetic(query) {
    var tc = new TokenConverter();
    try {
        var result = grammar_pegjs_1.default.parse(query, { tc: tc });
        return { result: result, error: tc.errors[0], tc: tc };
    }
    catch (error) {
        return { result: null, error: error.message, tc: tc };
    }
}
exports.parseArithmetic = parseArithmetic;
//# sourceMappingURL=parser.jsx.map