Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var queryString = tslib_1.__importStar(require("query-string"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var locale_1 = require("app/locale");
var fieldFromConfig_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/fieldFromConfig"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var DEBOUNCE_MS = 200;
/**
 * @abstract
 */
var AbstractExternalIssueForm = /** @class */ (function (_super) {
    tslib_1.__extends(AbstractExternalIssueForm, _super);
    function AbstractExternalIssueForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldRenderBadRequests = true;
        _this.refetchConfig = function () {
            var _a = _this.state, action = _a.action, dynamicFieldValues = _a.dynamicFieldValues;
            var query = tslib_1.__assign({ action: action }, dynamicFieldValues);
            var endpoint = _this.getEndPointString();
            _this.api.request(endpoint, {
                method: 'GET',
                query: query,
                success: function (data, _, resp) {
                    _this.handleRequestSuccess({ stateKey: 'integrationDetails', data: data, resp: resp }, true);
                },
                error: function (error) {
                    _this.handleError(error, ['integrationDetails', endpoint, null, null]);
                },
            });
        };
        _this.getConfigName = function () {
            // Explicitly returning a non-interpolated string for clarity.
            var action = _this.state.action;
            switch (action) {
                case 'create':
                    return 'createIssueConfig';
                case 'link':
                    return 'linkIssueConfig';
                default:
                    throw new Error('illegal action');
            }
        };
        /**
         * Convert IntegrationIssueConfig to an object that maps field names to the
         * values of fields where `updatesFrom` is true. This function prefers to read
         * configs from its parameters and otherwise falls back to reading from state.
         * @param integrationDetailsParam
         * @returns Object of field names to values.
         */
        _this.getDynamicFields = function (integrationDetailsParam) {
            var integrationDetailsFromState = _this.state.integrationDetails;
            var integrationDetails = integrationDetailsParam || integrationDetailsFromState;
            var config = (integrationDetails || {})[_this.getConfigName()];
            return Object.fromEntries((config || [])
                .filter(function (field) { return field.updatesForm; })
                .map(function (field) { return [field.name, field.default || null]; }));
        };
        _this.onRequestSuccess = function (_a) {
            var stateKey = _a.stateKey, data = _a.data;
            if (stateKey === 'integrationDetails') {
                _this.handleReceiveIntegrationDetails(data);
                _this.setState({
                    dynamicFieldValues: _this.getDynamicFields(data),
                });
            }
        };
        /**
         * If this field should updateFrom, updateForm. Otherwise, do nothing.
         */
        _this.onFieldChange = function (label, value) {
            var dynamicFieldValues = _this.state.dynamicFieldValues;
            var dynamicFields = _this.getDynamicFields();
            if (dynamicFields.hasOwnProperty(label) && dynamicFieldValues) {
                dynamicFieldValues[label] = value;
                _this.setState({
                    dynamicFieldValues: dynamicFieldValues,
                    reloading: true,
                    error: false,
                    remainingRequests: 1,
                }, _this.refetchConfig);
            }
        };
        /** For fields with dynamic fields, cache the fetched choices. */
        _this.updateFetchedFieldOptionsCache = function (field, result) {
            var _a;
            var fetchedFieldOptionsCache = _this.state.fetchedFieldOptionsCache;
            _this.setState({
                fetchedFieldOptionsCache: tslib_1.__assign(tslib_1.__assign({}, fetchedFieldOptionsCache), (_a = {}, _a[field.name] = result.map(function (obj) { return [obj.value, obj.label]; }), _a)),
            });
        };
        /**
         * Get the list of options for a field via debounced API call. For example,
         * the list of users that match the input string. The Promise rejects if there
         * are any errors.
         */
        _this.getOptions = function (field, input) {
            return new Promise(function (resolve, reject) {
                if (!input) {
                    return resolve(_this.getDefaultOptions(field));
                }
                return _this.debouncedOptionLoad(field, input, function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        _this.updateFetchedFieldOptionsCache(field, result);
                        resolve(result);
                    }
                });
            });
        };
        _this.debouncedOptionLoad = debounce_1.default(function (field, input, cb) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var dynamicFieldValues, query, url, separator, response, _a, _b, _c, err_1;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        dynamicFieldValues = this.state.dynamicFieldValues;
                        query = queryString.stringify(tslib_1.__assign(tslib_1.__assign({}, dynamicFieldValues), { field: field.name, query: input }));
                        url = field.url || '';
                        separator = url.includes('?') ? '&' : '?';
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 6, , 7]);
                        return [4 /*yield*/, fetch(url + separator + query)];
                    case 2:
                        response = _d.sent();
                        _a = cb;
                        _b = [null];
                        if (!response.ok) return [3 /*break*/, 4];
                        return [4 /*yield*/, response.json()];
                    case 3:
                        _c = _d.sent();
                        return [3 /*break*/, 5];
                    case 4:
                        _c = [];
                        _d.label = 5;
                    case 5:
                        _a.apply(void 0, _b.concat([_c]));
                        return [3 /*break*/, 7];
                    case 6:
                        err_1 = _d.sent();
                        cb(err_1);
                        return [3 /*break*/, 7];
                    case 7: return [2 /*return*/];
                }
            });
        }); }, DEBOUNCE_MS, { trailing: true });
        _this.getDefaultOptions = function (field) {
            var choices = field.choices || [];
            return choices.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), value = _b[0], label = _b[1];
                return ({ value: value, label: label });
            });
        };
        /** If this field is an async select (field.url is not null), add async props. */
        _this.getFieldProps = function (field) {
            return field.url
                ? {
                    async: true,
                    autoload: true,
                    cache: false,
                    loadOptions: function (input) { return _this.getOptions(field, input); },
                    defaultOptions: _this.getDefaultOptions(field),
                    onBlurResetsInput: false,
                    onCloseResetsInput: false,
                    onSelectResetsInput: false,
                }
                : {};
        };
        // Abstract methods.
        _this.handleReceiveIntegrationDetails = function (_data) {
            // Do nothing.
        };
        _this.renderNavTabs = function () { return null; };
        _this.renderBodyText = function () { return null; };
        _this.getTitle = function () { return locale_1.tct('Issue Link Settings', {}); };
        _this.getFormProps = function () {
            throw new Error("Method 'getFormProps()' must be implemented.");
        };
        _this.getDefaultFormProps = function () {
            return {
                footerClass: 'modal-footer',
                onFieldChange: _this.onFieldChange,
                submitDisabled: _this.state.reloading,
                // Other form props implemented by child classes.
            };
        };
        _this.getCleanedFields = function () {
            var _a = _this.state, fetchedFieldOptionsCache = _a.fetchedFieldOptionsCache, integrationDetails = _a.integrationDetails;
            var configsFromAPI = (integrationDetails || {})[_this.getConfigName()];
            return (configsFromAPI || []).map(function (field) {
                var fieldCopy = tslib_1.__assign({}, field);
                // Overwrite choices from cache.
                if (fetchedFieldOptionsCache === null || fetchedFieldOptionsCache === void 0 ? void 0 : fetchedFieldOptionsCache.hasOwnProperty(field.name)) {
                    fieldCopy.choices = fetchedFieldOptionsCache[field.name];
                }
                return fieldCopy;
            });
        };
        _this.renderForm = function (formFields) {
            var initialData = (formFields || []).reduce(function (accumulator, field) {
                accumulator[field.name] =
                    // Passing an empty array breaks MultiSelect.
                    field.multiple && field.default === [] ? '' : field.default;
                return accumulator;
            }, {});
            var _a = _this.props, Header = _a.Header, Body = _a.Body;
            return (<React.Fragment>
        <Header closeButton>{_this.getTitle()}</Header>
        {_this.renderNavTabs()}
        <Body>
          {_this.shouldRenderLoading() ? (_this.renderLoading()) : (<React.Fragment>
              {_this.renderBodyText()}
              <form_1.default initialData={initialData} {..._this.getFormProps()}>
                {(formFields || [])
                        .filter(function (field) { return field.hasOwnProperty('name'); })
                        .map(function (fields) { return (tslib_1.__assign(tslib_1.__assign({}, fields), { noOptionsMessage: function () { return 'No options. Type to search.'; } })); })
                        .map(function (field) { return (<fieldFromConfig_1.default disabled={_this.state.reloading} field={field} flexibleControlStateSize inline={false} key={field.name + "-" + field.default + "-" + field.required} stacked {..._this.getFieldProps(field)}/>); })}
              </form_1.default>
            </React.Fragment>)}
        </Body>
      </React.Fragment>);
        };
        return _this;
    }
    AbstractExternalIssueForm.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { action: 'create', dynamicFieldValues: null, fetchedFieldOptionsCache: {}, integrationDetails: null });
    };
    AbstractExternalIssueForm.prototype.getEndPointString = function () {
        throw new Error("Method 'getEndPointString()' must be implemented.");
    };
    AbstractExternalIssueForm.prototype.renderComponent = function () {
        return this.state.error
            ? this.renderError(new Error('Unable to load all required endpoints'))
            : this.renderBody();
    };
    return AbstractExternalIssueForm;
}(asyncComponent_1.default));
exports.default = AbstractExternalIssueForm;
//# sourceMappingURL=abstractExternalIssueForm.jsx.map