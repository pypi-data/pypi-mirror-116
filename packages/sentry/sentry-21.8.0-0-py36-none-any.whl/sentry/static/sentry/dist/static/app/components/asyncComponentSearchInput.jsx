Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
/**
 * This is a search input that can be easily used in AsyncComponent/Views.
 *
 * It probably doesn't make too much sense outside of an AsyncComponent atm.
 */
var AsyncComponentSearchInput = /** @class */ (function (_super) {
    tslib_1.__extends(AsyncComponentSearchInput, _super);
    function AsyncComponentSearchInput() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: '',
            busy: false,
        };
        _this.immediateQuery = function (searchQuery) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, location, api, _b, data, resp, _c;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, location = _a.location, api = _a.api;
                        this.setState({ busy: true });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("" + this.props.url, {
                                includeAllArgs: true,
                                method: 'GET',
                                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: searchQuery }),
                            })];
                    case 2:
                        _b = tslib_1.__read.apply(void 0, [_d.sent(), 3]), data = _b[0], resp = _b[2];
                        // only update data if the request's query matches the current query
                        if (this.state.query === searchQuery) {
                            this.props.onSuccess(data, resp);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        this.props.onError();
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ busy: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.query = debounce_1.default(_this.immediateQuery, _this.props.debounceWait);
        _this.handleChange = function (query) {
            _this.query(query);
            _this.setState({ query: query });
        };
        _this.handleInputChange = function (evt) {
            return _this.handleChange(evt.target.value);
        };
        /**
         * This is called when "Enter" (more specifically a form "submit" event) is pressed.
         */
        _this.handleSearch = function (evt) {
            var _a = _this.props, updateRoute = _a.updateRoute, onSearchSubmit = _a.onSearchSubmit;
            evt.preventDefault();
            // Update the URL to reflect search term.
            if (updateRoute) {
                var _b = _this.props, router = _b.router, location_1 = _b.location;
                router.push({
                    pathname: location_1.pathname,
                    query: {
                        query: _this.state.query,
                    },
                });
            }
            if (typeof onSearchSubmit !== 'function') {
                return;
            }
            onSearchSubmit(_this.state.query, evt);
        };
        return _this;
    }
    AsyncComponentSearchInput.prototype.render = function () {
        var _a = this.props, placeholder = _a.placeholder, children = _a.children, className = _a.className;
        var _b = this.state, busy = _b.busy, query = _b.query;
        var defaultSearchBar = (<Form onSubmit={this.handleSearch}>
        <input_1.default value={query} onChange={this.handleInputChange} className={className} placeholder={placeholder}/>
        {busy && <StyledLoadingIndicator size={18} hideMessage mini/>}
      </Form>);
        return children === undefined
            ? defaultSearchBar
            : children({ defaultSearchBar: defaultSearchBar, busy: busy, value: query, handleChange: this.handleChange });
    };
    AsyncComponentSearchInput.defaultProps = {
        placeholder: locale_1.t('Search...'),
        debounceWait: 200,
    };
    return AsyncComponentSearchInput;
}(React.Component));
var StyledLoadingIndicator = styled_1.default(loadingIndicator_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  right: 25px;\n  top: 50%;\n  transform: translateY(-13px);\n"], ["\n  position: absolute;\n  right: 25px;\n  top: 50%;\n  transform: translateY(-13px);\n"])));
var Form = styled_1.default('form')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
exports.default = ReactRouter.withRouter(AsyncComponentSearchInput);
var templateObject_1, templateObject_2;
//# sourceMappingURL=asyncComponentSearchInput.jsx.map