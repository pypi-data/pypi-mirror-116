Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectContext = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var members_1 = require("app/actionCreators/members");
var projects_1 = require("app/actionCreators/projects");
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var missingProjectMembership_1 = tslib_1.__importDefault(require("app/components/projects/missingProjectMembership"));
var locale_1 = require("app/locale");
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var ErrorTypes;
(function (ErrorTypes) {
    ErrorTypes["MISSING_MEMBERSHIP"] = "MISSING_MEMBERSHIP";
    ErrorTypes["PROJECT_NOT_FOUND"] = "PROJECT_NOT_FOUND";
    ErrorTypes["UNKNOWN"] = "UNKNOWN";
})(ErrorTypes || (ErrorTypes = {}));
/**
 * Higher-order component that sets `project` as a child context
 * value to be accessed by child elements.
 *
 * Additionally delays rendering of children until project XHR has finished
 * and context is populated.
 */
var ProjectContext = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectContext, _super);
    function ProjectContext() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.docTitleRef = react_1.createRef();
        _this.unsubscribeProjects = projectsStore_1.default.listen(function (projectIds) { return _this.onProjectChange(projectIds); }, undefined);
        _this.unsubscribeMembers = memberListStore_1.default.listen(function (memberList) { return _this.setState({ memberList: memberList }); }, undefined);
        return _this;
    }
    ProjectContext.prototype.getInitialState = function () {
        return {
            loading: true,
            error: false,
            errorType: null,
            memberList: [],
            project: null,
        };
    };
    ProjectContext.prototype.getChildContext = function () {
        return {
            project: this.state.project,
        };
    };
    ProjectContext.prototype.componentWillMount = function () {
        this.fetchData();
    };
    ProjectContext.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.projectId === this.props.projectId) {
            return;
        }
        if (!nextProps.skipReload) {
            this.remountComponent();
        }
    };
    ProjectContext.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevProps.projectId !== this.props.projectId) {
            this.fetchData();
        }
        // Project list has changed. Likely indicating that a new project has been
        // added. Re-fetch project details in case that the new project is the active
        // project.
        //
        // For now, only compare lengths. It is possible that project slugs within
        // the list could change, but it doesn't seem to be broken anywhere else at
        // the moment that would require deeper checks.
        if (prevProps.projects.length !== this.props.projects.length) {
            this.fetchData();
        }
        // Call forceUpdate() on <DocumentTitle/> if either project or organization
        // state has changed. This is because <DocumentTitle/>'s shouldComponentUpdate()
        // returns false unless props differ; meaning context changes for project/org
        // do NOT trigger renders for <DocumentTitle/> OR any subchildren. The end result
        // being that child elements that listen for context changes on project/org will
        // NOT update (without this hack).
        // See: https://github.com/gaearon/react-document-title/issues/35
        // intentionally shallow comparing references
        if (prevState.project !== this.state.project) {
            var docTitle = this.docTitleRef.current;
            if (!docTitle) {
                return;
            }
            docTitle.forceUpdate();
        }
    };
    ProjectContext.prototype.componentWillUnmount = function () {
        this.unsubscribeMembers();
        this.unsubscribeProjects();
    };
    ProjectContext.prototype.remountComponent = function () {
        this.setState(this.getInitialState());
    };
    ProjectContext.prototype.getTitle = function () {
        var _a, _b;
        return (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.slug) !== null && _b !== void 0 ? _b : 'Sentry';
    };
    ProjectContext.prototype.onProjectChange = function (projectIds) {
        if (!this.state.project) {
            return;
        }
        if (!projectIds.has(this.state.project.id)) {
            return;
        }
        this.setState({
            project: tslib_1.__assign({}, projectsStore_1.default.getById(this.state.project.id)),
        });
    };
    ProjectContext.prototype.identifyProject = function () {
        var _a = this.props, projects = _a.projects, projectId = _a.projectId;
        var projectSlug = projectId;
        return projects.find(function (_a) {
            var slug = _a.slug;
            return slug === projectSlug;
        }) || null;
    };
    ProjectContext.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, orgId, projectId, skipReload, activeProject, hasAccess, projectRequest, project, error_1, error_2;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, orgId = _a.orgId, projectId = _a.projectId, skipReload = _a.skipReload;
                        activeProject = this.identifyProject();
                        hasAccess = activeProject && activeProject.hasAccess;
                        this.setState(function (state) { return ({
                            // if `skipReload` is true, then don't change loading state
                            loading: skipReload ? state.loading : true,
                            // we bind project initially, but it'll rebind
                            project: activeProject,
                        }); });
                        if (!(activeProject && hasAccess)) return [3 /*break*/, 5];
                        projects_1.setActiveProject(null);
                        projectRequest = this.props.api.requestPromise("/projects/" + orgId + "/" + projectId + "/");
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projectRequest];
                    case 2:
                        project = _b.sent();
                        this.setState({
                            loading: false,
                            project: project,
                            error: false,
                            errorType: null,
                        });
                        // assuming here that this means the project is considered the active project
                        projects_1.setActiveProject(project);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({
                            loading: false,
                            error: false,
                            errorType: ErrorTypes.UNKNOWN,
                        });
                        return [3 /*break*/, 4];
                    case 4:
                        members_1.fetchOrgMembers(this.props.api, orgId, [activeProject.id]);
                        return [2 /*return*/];
                    case 5:
                        // User is not a memberof the active project
                        if (activeProject && !activeProject.isMember) {
                            this.setState({
                                loading: false,
                                error: true,
                                errorType: ErrorTypes.MISSING_MEMBERSHIP,
                            });
                            return [2 /*return*/];
                        }
                        _b.label = 6;
                    case 6:
                        _b.trys.push([6, 8, , 9]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + orgId + "/" + projectId + "/")];
                    case 7:
                        _b.sent();
                        return [3 /*break*/, 9];
                    case 8:
                        error_2 = _b.sent();
                        this.setState({
                            loading: false,
                            error: true,
                            errorType: ErrorTypes.PROJECT_NOT_FOUND,
                        });
                        return [3 /*break*/, 9];
                    case 9: return [2 /*return*/];
                }
            });
        });
    };
    ProjectContext.prototype.renderBody = function () {
        var _a = this.state, error = _a.error, errorType = _a.errorType, loading = _a.loading, project = _a.project;
        if (loading) {
            return (<div className="loading-full-layout">
          <loadingIndicator_1.default />
        </div>);
        }
        if (!error && project) {
            var children = this.props.children;
            return typeof children === 'function' ? children({ project: project }) : children;
        }
        switch (errorType) {
            case ErrorTypes.PROJECT_NOT_FOUND:
                // TODO(chrissy): use scale for margin values
                return (<div className="container">
            <div className="alert alert-block" style={{ margin: '30px 0 10px' }}>
              {locale_1.t('The project you were looking for was not found.')}
            </div>
          </div>);
            case ErrorTypes.MISSING_MEMBERSHIP:
                // TODO(dcramer): add various controls to improve this flow and break it
                // out into a reusable missing access error component
                return (<ErrorWrapper>
            <missingProjectMembership_1.default organization={this.props.organization} projectSlug={project === null || project === void 0 ? void 0 : project.slug}/>
          </ErrorWrapper>);
            default:
                return <loadingError_1.default onRetry={this.remountComponent}/>;
        }
    };
    ProjectContext.prototype.render = function () {
        return (<react_document_title_1.default ref={this.docTitleRef} title={this.getTitle()}>
        {this.renderBody()}
      </react_document_title_1.default>);
    };
    ProjectContext.childContextTypes = {
        project: sentryTypes_1.default.Project,
    };
    return ProjectContext;
}(react_1.Component));
exports.ProjectContext = ProjectContext;
exports.default = withApi_1.default(withOrganization_1.default(withProjects_1.default(ProjectContext)));
var ErrorWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  margin: ", " ", ";\n"], ["\n  width: 100%;\n  margin: ", " ", ";\n"])), space_1.default(2), space_1.default(4));
var templateObject_1;
//# sourceMappingURL=projectContext.jsx.map