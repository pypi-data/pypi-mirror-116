Object.defineProperty(exports, "__esModule", { value: true });
exports.batchedPromptsCheck = exports.promptsCheck = exports.promptsUpdate = void 0;
var tslib_1 = require("tslib");
/**
 * Update the status of a prompt
 */
function promptsUpdate(api, params) {
    return api.requestPromise('/prompts-activity/', {
        method: 'PUT',
        data: {
            organization_id: params.organizationId,
            project_id: params.projectId,
            feature: params.feature,
            status: params.status,
        },
    });
}
exports.promptsUpdate = promptsUpdate;
/**
 * Get the status of a prompt
 */
function promptsCheck(api, params) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var query, response, data;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    query = tslib_1.__assign({ feature: params.feature, organization_id: params.organizationId }, (params.projectId === undefined ? {} : { project_id: params.projectId }));
                    return [4 /*yield*/, api.requestPromise('/prompts-activity/', {
                            query: query,
                        })];
                case 1:
                    response = _a.sent();
                    data = response === null || response === void 0 ? void 0 : response.data;
                    if (!data) {
                        return [2 /*return*/, null];
                    }
                    return [2 /*return*/, {
                            dismissedTime: data.dismissed_ts,
                            snoozedTime: data.snoozed_ts,
                        }];
            }
        });
    });
}
exports.promptsCheck = promptsCheck;
/**
 * Get the status of many prompt
 */
function batchedPromptsCheck(api, features, params) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var query, response, responseFeatures, result, features_1, features_1_1, featureName, item;
        var e_1, _a;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    query = tslib_1.__assign({ feature: features, organization_id: params.organizationId }, (params.projectId === undefined ? {} : { project_id: params.projectId }));
                    return [4 /*yield*/, api.requestPromise('/prompts-activity/', {
                            query: query,
                        })];
                case 1:
                    response = _b.sent();
                    responseFeatures = response === null || response === void 0 ? void 0 : response.features;
                    result = {};
                    if (!responseFeatures) {
                        return [2 /*return*/, result];
                    }
                    try {
                        for (features_1 = tslib_1.__values(features), features_1_1 = features_1.next(); !features_1_1.done; features_1_1 = features_1.next()) {
                            featureName = features_1_1.value;
                            item = responseFeatures[featureName];
                            if (item) {
                                result[featureName] = {
                                    dismissedTime: item.dismissed_ts,
                                    snoozedTime: item.snoozed_ts,
                                };
                            }
                            else {
                                result[featureName] = null;
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (features_1_1 && !features_1_1.done && (_a = features_1.return)) _a.call(features_1);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                    return [2 /*return*/, result];
            }
        });
    });
}
exports.batchedPromptsCheck = batchedPromptsCheck;
//# sourceMappingURL=prompts.jsx.map