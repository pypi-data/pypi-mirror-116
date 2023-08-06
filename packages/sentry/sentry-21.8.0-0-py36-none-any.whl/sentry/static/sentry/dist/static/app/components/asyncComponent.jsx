Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var prop_types_1 = tslib_1.__importDefault(require("prop-types"));
var api_1 = require("app/api");
var asyncComponentSearchInput_1 = tslib_1.__importDefault(require("app/components/asyncComponentSearchInput"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var permissionDenied_1 = tslib_1.__importDefault(require("app/views/permissionDenied"));
var routeError_1 = tslib_1.__importDefault(require("app/views/routeError"));
/**
 * Wraps methods on the AsyncComponent to catch errors and set the `error`
 * state on error.
 */
function wrapErrorHandling(component, fn) {
    return function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        try {
            return fn.apply(void 0, tslib_1.__spreadArray([], tslib_1.__read(args)));
        }
        catch (error) {
            // eslint-disable-next-line no-console
            console.error(error);
            setTimeout(function () {
                throw error;
            });
            component.setState({ error: error });
            return null;
        }
    };
}
var AsyncComponent = /** @class */ (function (_super) {
    tslib_1.__extends(AsyncComponent, _super);
    function AsyncComponent(props, context) {
        var _this = _super.call(this, props, context) || this;
        // Override this flag to have the component reload it's state when the window
        // becomes visible again. This will set the loading and reloading state, but
        // will not render a loading state during reloading.
        //
        // eslint-disable-next-line react/sort-comp
        _this.reloadOnVisible = false;
        // When enabling reloadOnVisible, this flag may be used to turn on and off
        // the reloading. This is useful if your component only needs to reload when
        // becoming visible during certain states.
        //
        // eslint-disable-next-line react/sort-comp
        _this.shouldReloadOnVisible = false;
        // This affects how the component behaves when `remountComponent` is called
        // By default, the component gets put back into a "loading" state when re-fetching data.
        // If this is true, then when we fetch data, the original ready component remains mounted
        // and it will need to handle any additional "reloading" states
        _this.shouldReload = false;
        // should `renderError` render the `detail` attribute of a 400 error
        _this.shouldRenderBadRequests = false;
        _this.api = new api_1.Client();
        // Check if we should measure render time for this component
        _this.markShouldMeasure = function (_a) {
            var _b = _a === void 0 ? {} : _a, remainingRequests = _b.remainingRequests, error = _b.error;
            if (!_this._measurement.hasMeasured) {
                _this._measurement.finished = remainingRequests === 0;
                _this._measurement.error = error || _this._measurement.error;
            }
        };
        _this.remountComponent = function () {
            if (_this.shouldReload) {
                _this.reloadData();
            }
            else {
                _this.setState(_this.getDefaultState(), _this.fetchData);
            }
        };
        _this.visibilityReloader = function () {
            return _this.shouldReloadOnVisible &&
                !_this.state.loading &&
                !document.hidden &&
                _this.reloadData();
        };
        _this.fetchData = function (extraState) {
            var endpoints = _this.getEndpoints();
            if (!endpoints.length) {
                _this.setState({ loading: false, error: false });
                return;
            }
            // Cancel any in flight requests
            _this.api.clear();
            _this.setState(tslib_1.__assign({ loading: true, error: false, remainingRequests: endpoints.length }, extraState));
            endpoints.forEach(function (_a) {
                var _b = tslib_1.__read(_a, 4), stateKey = _b[0], endpoint = _b[1], params = _b[2], options = _b[3];
                options = options || {};
                // If you're using nested async components/views make sure to pass the
                // props through so that the child component has access to props.location
                var locationQuery = (_this.props.location && _this.props.location.query) || {};
                var query = (params && params.query) || {};
                // If paginate option then pass entire `query` object to API call
                // It should only be expecting `query.cursor` for pagination
                if ((options.paginate || locationQuery.cursor) && !options.disableEntireQuery) {
                    query = tslib_1.__assign(tslib_1.__assign({}, locationQuery), query);
                }
                _this.api.request(endpoint, tslib_1.__assign(tslib_1.__assign({ method: 'GET' }, params), { query: query, success: function (data, _, resp) {
                        _this.handleRequestSuccess({ stateKey: stateKey, data: data, resp: resp }, true);
                    }, error: function (error) {
                        // Allow endpoints to fail
                        // allowError can have side effects to handle the error
                        if (options.allowError && options.allowError(error)) {
                            error = null;
                        }
                        _this.handleError(error, [stateKey, endpoint, params, options]);
                    } }));
            });
        };
        _this.fetchData = wrapErrorHandling(_this, _this.fetchData.bind(_this));
        _this.render = wrapErrorHandling(_this, _this.render.bind(_this));
        _this.state = _this.getDefaultState();
        _this._measurement = {
            hasMeasured: false,
        };
        if (props.routes && props.routes) {
            analytics_1.metric.mark({ name: "async-component-" + getRouteStringFromRoutes_1.default(props.routes) });
        }
        return _this;
    }
    AsyncComponent.prototype.UNSAFE_componentWillMount = function () {
        this.api = new api_1.Client();
        this.fetchData();
        if (this.reloadOnVisible) {
            document.addEventListener('visibilitychange', this.visibilityReloader);
        }
    };
    // Compatibility shim for child classes that call super on this hook.
    AsyncComponent.prototype.UNSAFE_componentWillReceiveProps = function (_newProps, _newContext) { };
    AsyncComponent.prototype.componentDidUpdate = function (prevProps, prevContext) {
        var isRouterInContext = !!prevContext.router;
        var isLocationInProps = prevProps.location !== undefined;
        var currentLocation = isLocationInProps
            ? this.props.location
            : isRouterInContext
                ? this.context.router.location
                : null;
        var prevLocation = isLocationInProps
            ? prevProps.location
            : isRouterInContext
                ? prevContext.router.location
                : null;
        if (!(currentLocation && prevLocation)) {
            return;
        }
        // Take a measurement from when this component is initially created until it finishes it's first
        // set of API requests
        if (!this._measurement.hasMeasured &&
            this._measurement.finished &&
            this.props.routes) {
            var routeString = getRouteStringFromRoutes_1.default(this.props.routes);
            analytics_1.metric.measure({
                name: 'app.component.async-component',
                start: "async-component-" + routeString,
                data: {
                    route: routeString,
                    error: this._measurement.error,
                },
            });
            this._measurement.hasMeasured = true;
        }
        // Re-fetch data when router params change.
        if (!isEqual_1.default(this.props.params, prevProps.params) ||
            currentLocation.search !== prevLocation.search ||
            currentLocation.state !== prevLocation.state) {
            this.remountComponent();
        }
    };
    AsyncComponent.prototype.componentWillUnmount = function () {
        this.api.clear();
        document.removeEventListener('visibilitychange', this.visibilityReloader);
    };
    // XXX: can't call this getInitialState as React whines
    AsyncComponent.prototype.getDefaultState = function () {
        var endpoints = this.getEndpoints();
        var state = {
            // has all data finished requesting?
            loading: true,
            // is the component reload
            reloading: false,
            // is there an error loading ANY data?
            error: false,
            errors: {},
        };
        endpoints.forEach(function (_a) {
            var _b = tslib_1.__read(_a, 2), stateKey = _b[0], _endpoint = _b[1];
            state[stateKey] = null;
        });
        return state;
    };
    AsyncComponent.prototype.reloadData = function () {
        this.fetchData({ reloading: true });
    };
    AsyncComponent.prototype.onRequestSuccess = function (_resp /* {stateKey, data, resp} */) {
        // Allow children to implement this
    };
    AsyncComponent.prototype.onRequestError = function (_resp, _args) {
        // Allow children to implement this
    };
    AsyncComponent.prototype.onLoadAllEndpointsSuccess = function () {
        // Allow children to implement this
    };
    AsyncComponent.prototype.handleRequestSuccess = function (_a, initialRequest) {
        var _this = this;
        var stateKey = _a.stateKey, data = _a.data, resp = _a.resp;
        this.setState(function (prevState) {
            var _a;
            var state = (_a = {},
                _a[stateKey] = data,
                // TODO(billy): This currently fails if this request is retried by SudoModal
                _a[stateKey + "PageLinks"] = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link'),
                _a);
            if (initialRequest) {
                state.remainingRequests = prevState.remainingRequests - 1;
                state.loading = prevState.remainingRequests > 1;
                state.reloading = prevState.reloading && state.loading;
                _this.markShouldMeasure({ remainingRequests: state.remainingRequests });
            }
            return state;
        }, function () {
            // if everything is loaded and we don't have an error, call the callback
            if (_this.state.remainingRequests === 0 && !_this.state.error) {
                _this.onLoadAllEndpointsSuccess();
            }
        });
        this.onRequestSuccess({ stateKey: stateKey, data: data, resp: resp });
    };
    AsyncComponent.prototype.handleError = function (error, args) {
        var _this = this;
        var _a = tslib_1.__read(args, 1), stateKey = _a[0];
        if (error && error.responseText) {
            Sentry.addBreadcrumb({
                message: error.responseText,
                category: 'xhr',
                level: Sentry.Severity.Error,
            });
        }
        this.setState(function (prevState) {
            var _a, _b;
            var loading = prevState.remainingRequests > 1;
            var state = (_a = {},
                _a[stateKey] = null,
                _a.errors = tslib_1.__assign(tslib_1.__assign({}, prevState.errors), (_b = {}, _b[stateKey] = error, _b)),
                _a.error = prevState.error || !!error,
                _a.remainingRequests = prevState.remainingRequests - 1,
                _a.loading = loading,
                _a.reloading = prevState.reloading && loading,
                _a);
            _this.markShouldMeasure({ remainingRequests: state.remainingRequests, error: true });
            return state;
        });
        this.onRequestError(error, args);
    };
    /**
     * @deprecated use getEndpoints
     */
    AsyncComponent.prototype.getEndpointParams = function () {
        // eslint-disable-next-line no-console
        console.warn('getEndpointParams is deprecated');
        return {};
    };
    /**
     * @deprecated use getEndpoints
     */
    AsyncComponent.prototype.getEndpoint = function () {
        // eslint-disable-next-line no-console
        console.warn('getEndpoint is deprecated');
        return null;
    };
    /**
     * Return a list of endpoint queries to make.
     *
     * return [
     *   ['stateKeyName', '/endpoint/', {optional: 'query params'}, {options}]
     * ]
     */
    AsyncComponent.prototype.getEndpoints = function () {
        var endpoint = this.getEndpoint();
        if (!endpoint) {
            return [];
        }
        return [['data', endpoint, this.getEndpointParams()]];
    };
    AsyncComponent.prototype.renderSearchInput = function (_a) {
        var _this = this;
        var stateKey = _a.stateKey, url = _a.url, props = tslib_1.__rest(_a, ["stateKey", "url"]);
        var _b = tslib_1.__read(this.getEndpoints() || [null], 1), firstEndpoint = _b[0];
        var stateKeyOrDefault = stateKey || (firstEndpoint && firstEndpoint[0]);
        var urlOrDefault = url || (firstEndpoint && firstEndpoint[1]);
        return (<asyncComponentSearchInput_1.default url={urlOrDefault} {...props} api={this.api} onSuccess={function (data, resp) {
                _this.handleRequestSuccess({ stateKey: stateKeyOrDefault, data: data, resp: resp });
            }} onError={function () {
                _this.renderError(new Error('Error with AsyncComponentSearchInput'));
            }}/>);
    };
    AsyncComponent.prototype.renderLoading = function () {
        return <loadingIndicator_1.default />;
    };
    AsyncComponent.prototype.renderError = function (error, disableLog, disableReport) {
        if (disableLog === void 0) { disableLog = false; }
        if (disableReport === void 0) { disableReport = false; }
        var errors = this.state.errors;
        // 401s are captured by SudoModal, but may be passed back to AsyncComponent if they close the modal without identifying
        var unauthorizedErrors = Object.values(errors).find(function (resp) { return resp && resp.status === 401; });
        // Look through endpoint results to see if we had any 403s, means their role can not access resource
        var permissionErrors = Object.values(errors).find(function (resp) { return resp && resp.status === 403; });
        // If all error responses have status code === 0, then show error message but don't
        // log it to sentry
        var shouldLogSentry = !!Object.values(errors).find(function (resp) { return resp && resp.status !== 0; }) || disableLog;
        if (unauthorizedErrors) {
            return (<loadingError_1.default message={locale_1.t('You are not authorized to access this resource.')}/>);
        }
        if (permissionErrors) {
            return <permissionDenied_1.default />;
        }
        if (this.shouldRenderBadRequests) {
            var badRequests = Object.values(errors)
                .filter(function (resp) {
                return resp && resp.status === 400 && resp.responseJSON && resp.responseJSON.detail;
            })
                .map(function (resp) { return resp.responseJSON.detail; });
            if (badRequests.length) {
                return <loadingError_1.default message={tslib_1.__spreadArray([], tslib_1.__read(new Set(badRequests))).join('\n')}/>;
            }
        }
        return (<routeError_1.default error={error} disableLogSentry={!shouldLogSentry} disableReport={disableReport}/>);
    };
    AsyncComponent.prototype.shouldRenderLoading = function () {
        var _a = this.state, loading = _a.loading, reloading = _a.reloading;
        return loading && (!this.shouldReload || !reloading);
    };
    AsyncComponent.prototype.renderComponent = function () {
        return this.shouldRenderLoading()
            ? this.renderLoading()
            : this.state.error
                ? this.renderError(new Error('Unable to load all required endpoints'))
                : this.renderBody();
    };
    /**
     * Renders once all endpoints have been loaded
     */
    AsyncComponent.prototype.renderBody = function () {
        // Allow children to implement this
        throw new Error('Not implemented');
    };
    AsyncComponent.prototype.render = function () {
        return this.renderComponent();
    };
    AsyncComponent.contextTypes = {
        router: prop_types_1.default.object,
    };
    return AsyncComponent;
}(React.Component));
exports.default = AsyncComponent;
//# sourceMappingURL=asyncComponent.jsx.map