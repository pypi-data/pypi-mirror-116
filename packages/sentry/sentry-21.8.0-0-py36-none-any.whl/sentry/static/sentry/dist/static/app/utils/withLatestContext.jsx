Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var latestContextStore_1 = tslib_1.__importDefault(require("app/stores/latestContextStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var fallbackContext = {
    organization: null,
    project: null,
    lastRoute: null,
};
function withLatestContext(WrappedComponent) {
    var WithLatestContext = /** @class */ (function (_super) {
        tslib_1.__extends(WithLatestContext, _super);
        function WithLatestContext() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                latestContext: latestContextStore_1.default.get(),
            };
            _this.unsubscribe = latestContextStore_1.default.listen(function (latestContext) { return _this.setState({ latestContext: latestContext }); }, undefined);
            return _this;
        }
        WithLatestContext.prototype.componentWillUmount = function () {
            this.unsubscribe();
        };
        WithLatestContext.prototype.render = function () {
            var organizations = this.props.organizations;
            var latestContext = this.state.latestContext;
            var _a = latestContext || fallbackContext, organization = _a.organization, project = _a.project, lastRoute = _a.lastRoute;
            // Even though org details exists in LatestContextStore,
            // fetch organization from OrganizationsStore so that we can
            // expect consistent data structure because OrganizationsStore has a list
            // of orgs but not full org details
            var latestOrganization = organization ||
                (organizations && organizations.length
                    ? organizations.find(function (_a) {
                        var slug = _a.slug;
                        return slug === configStore_1.default.get('lastOrganization');
                    }) || organizations[0]
                    : null);
            // TODO(billy): Below is going to be wrong if component is passed project, it will override
            // project from `latestContext`
            return (<WrappedComponent project={project} lastRoute={lastRoute} {...this.props} organization={(this.props.organization || latestOrganization)}/>);
        };
        WithLatestContext.displayName = "withLatestContext(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithLatestContext;
    }(React.Component));
    return withOrganizations_1.default(WithLatestContext);
}
exports.default = withLatestContext;
//# sourceMappingURL=withLatestContext.jsx.map