Object.defineProperty(exports, "__esModule", { value: true });
exports.toggleKeyTransaction = exports.fetchTeamKeyTransactions = exports.fetchLegacyKeyTransactionsCount = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var locale_1 = require("app/locale");
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
function fetchLegacyKeyTransactionsCount(orgSlug) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var api, url, _a, data;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new api_1.Client();
                    url = "/organizations/" + orgSlug + "/legacy-key-transactions-count/";
                    return [4 /*yield*/, api.requestPromise(url, {
                            method: 'GET',
                            includeAllArgs: true,
                        })];
                case 1:
                    _a = tslib_1.__read.apply(void 0, [_b.sent(), 1]), data = _a[0];
                    return [2 /*return*/, data.keyed];
            }
        });
    });
}
exports.fetchLegacyKeyTransactionsCount = fetchLegacyKeyTransactionsCount;
function fetchTeamKeyTransactions(api, orgSlug, teams, projects) {
    var _a, _b, _c, _d, _e, _f;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var url, datas, cursor, hasMore, payload, _g, data, resp, pageLinks, paginationObject, err_1;
        return tslib_1.__generator(this, function (_h) {
            switch (_h.label) {
                case 0:
                    url = "/organizations/" + orgSlug + "/key-transactions-list/";
                    datas = [];
                    cursor = undefined;
                    hasMore = true;
                    _h.label = 1;
                case 1:
                    if (!hasMore) return [3 /*break*/, 6];
                    _h.label = 2;
                case 2:
                    _h.trys.push([2, 4, , 5]);
                    payload = { cursor: cursor, team: teams, project: projects };
                    if (!payload.cursor) {
                        delete payload.cursor;
                    }
                    if (!((_a = payload.project) === null || _a === void 0 ? void 0 : _a.length)) {
                        delete payload.project;
                    }
                    return [4 /*yield*/, api.requestPromise(url, {
                            method: 'GET',
                            includeAllArgs: true,
                            query: payload,
                        })];
                case 3:
                    _g = tslib_1.__read.apply(void 0, [_h.sent(), 3]), data = _g[0], resp = _g[2];
                    datas.push(data);
                    pageLinks = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link');
                    if (pageLinks) {
                        paginationObject = parseLinkHeader_1.default(pageLinks);
                        hasMore = (_c = (_b = paginationObject === null || paginationObject === void 0 ? void 0 : paginationObject.next) === null || _b === void 0 ? void 0 : _b.results) !== null && _c !== void 0 ? _c : false;
                        cursor = (_d = paginationObject.next) === null || _d === void 0 ? void 0 : _d.cursor;
                    }
                    else {
                        hasMore = false;
                    }
                    return [3 /*break*/, 5];
                case 4:
                    err_1 = _h.sent();
                    indicator_1.addErrorMessage((_f = (_e = err_1.responseJSON) === null || _e === void 0 ? void 0 : _e.detail) !== null && _f !== void 0 ? _f : locale_1.t('Error fetching team key transactions'));
                    throw err_1;
                case 5: return [3 /*break*/, 1];
                case 6: return [2 /*return*/, datas.flat()];
            }
        });
    });
}
exports.fetchTeamKeyTransactions = fetchTeamKeyTransactions;
function toggleKeyTransaction(api, isKeyTransaction, orgId, projects, transactionName, teamIds // TODO(txiao): make this required
) {
    indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
    var promise = api.requestPromise("/organizations/" + orgId + "/key-transactions/", {
        method: isKeyTransaction ? 'DELETE' : 'POST',
        query: {
            project: projects.map(function (id) { return String(id); }),
        },
        data: {
            transaction: transactionName,
            team: teamIds,
        },
    });
    promise.then(indicator_1.clearIndicators);
    promise.catch(function (response) {
        var _a;
        var responseJSON = response === null || response === void 0 ? void 0 : response.responseJSON;
        var errorDetails = (_a = responseJSON === null || responseJSON === void 0 ? void 0 : responseJSON.detail) !== null && _a !== void 0 ? _a : responseJSON === null || responseJSON === void 0 ? void 0 : responseJSON.non_field_errors;
        if (Array.isArray(errorDetails) && errorDetails.length && errorDetails[0]) {
            indicator_1.addErrorMessage(errorDetails[0]);
        }
        else {
            indicator_1.addErrorMessage(errorDetails !== null && errorDetails !== void 0 ? errorDetails : locale_1.t('Unable to update key transaction'));
        }
    });
    return promise;
}
exports.toggleKeyTransaction = toggleKeyTransaction;
//# sourceMappingURL=performance.jsx.map