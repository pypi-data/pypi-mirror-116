Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var detailedError_1 = tslib_1.__importDefault(require("app/components/errors/detailedError"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
/**
 * This component performs a client-side redirect to Event Details given only
 * an event ID (which normally additionally requires the event's Issue/Group ID).
 * It does this by using an XHR against the identically-named ProjectEventRedirect
 * _Django_ view, which responds with a 302 with the Location of the corresponding
 * Event Details page (if it exists).
 *
 * See:
 * https://github.com/getsentry/sentry/blob/824c03089907ad22a9282303a5eaca33989ce481/src/sentry/web/urls.py#L578
 */
var ProjectEventRedirect = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectEventRedirect, _super);
    function ProjectEventRedirect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: null,
        };
        return _this;
    }
    ProjectEventRedirect.prototype.componentDidMount = function () {
        var _this = this;
        var router = this.props.router;
        // This presumes that _this_ React view/route is only reachable at
        // /:org/:project/events/:eventId (the same URL which serves the ProjectEventRedirect
        // Django view).
        var endpoint = router.location.pathname;
        // Use XmlHttpRequest directly instead of our client API helper (fetch),
        // because you can't reach the underlying XHR via $.ajax, and we need
        // access to `xhr.responseURL`.
        //
        // TODO(epurkhiser): We can likely replace tihs with fetch
        var xhr = new XMLHttpRequest();
        // Hitting this endpoint will return a 302 with a new location, which
        // the XHR will follow and make a _second_ request. Using HEAD instead
        // of GET returns an empty response instead of the entire HTML content.
        xhr.open('HEAD', endpoint);
        xhr.send();
        xhr.onload = function () {
            if (xhr.status === 404) {
                _this.setState({ error: locale_1.t('Could not find an issue for the provided event id') });
                return;
            }
            // responseURL is the URL of the document the browser ultimately loaded,
            // after following any redirects. It _should_ be the page we're trying
            // to reach; use the router to go there.
            // Use `replace` so that hitting the browser back button will skip all
            // this redirect business.
            router.replace(xhr.responseURL);
        };
        xhr.onerror = function () {
            _this.setState({ error: locale_1.t('Could not load the requested event') });
        };
    };
    ProjectEventRedirect.prototype.render = function () {
        return this.state.error ? (<detailedError_1.default heading={locale_1.t('Not found')} message={this.state.error} hideSupportLinks/>) : (<organization_1.PageContent />);
    };
    return ProjectEventRedirect;
}(react_1.Component));
exports.default = ProjectEventRedirect;
//# sourceMappingURL=projectEventRedirect.jsx.map