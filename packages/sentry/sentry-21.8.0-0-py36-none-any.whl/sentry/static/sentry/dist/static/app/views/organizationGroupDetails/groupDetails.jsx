Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var ReactRouter = tslib_1.__importStar(require("react-router"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var prop_types_1 = tslib_1.__importDefault(require("prop-types"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var missingProjectMembership_1 = tslib_1.__importDefault(require("app/components/projects/missingProjectMembership"));
var locale_1 = require("app/locale");
var sentryTypes_1 = tslib_1.__importDefault(require("app/sentryTypes"));
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var organization_1 = require("app/styles/organization");
var callIfFunction_1 = require("app/utils/callIfFunction");
var events_1 = require("app/utils/events");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var constants_1 = require("./constants");
var header_1 = tslib_1.__importStar(require("./header"));
var utils_1 = require("./utils");
var GroupDetails = /** @class */ (function (_super) {
    tslib_1.__extends(GroupDetails, _super);
    function GroupDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.initialState;
        _this.remountComponent = function () {
            _this.setState(_this.initialState);
            _this.fetchData();
        };
        _this.refetchGroup = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, loadingGroup, loading, loadingEvent, group, api, updatedGroup, reprocessingNewRoute, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.state, loadingGroup = _a.loadingGroup, loading = _a.loading, loadingEvent = _a.loadingEvent, group = _a.group;
                        if ((group === null || group === void 0 ? void 0 : group.status) !== utils_1.ReprocessingStatus.REPROCESSING ||
                            loadingGroup ||
                            loading ||
                            loadingEvent) {
                            return [2 /*return*/];
                        }
                        api = this.props.api;
                        this.setState({ loadingGroup: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(this.groupDetailsEndpoint, {
                                query: this.getGroupQuery(),
                            })];
                    case 2:
                        updatedGroup = _b.sent();
                        reprocessingNewRoute = this.getReprocessingNewRoute(updatedGroup);
                        if (reprocessingNewRoute) {
                            ReactRouter.browserHistory.push(reprocessingNewRoute);
                            return [2 /*return*/];
                        }
                        this.setState({ group: updatedGroup, loadingGroup: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.handleRequestError(error_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.listener = groupStore_1.default.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        _this.interval = undefined;
        return _this;
    }
    GroupDetails.prototype.getChildContext = function () {
        return {
            group: this.state.group,
            location: this.props.location,
        };
    };
    GroupDetails.prototype.componentDidMount = function () {
        this.fetchData();
        this.updateReprocessingProgress();
    };
    GroupDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a, _b;
        if (prevProps.isGlobalSelectionReady !== this.props.isGlobalSelectionReady ||
            prevProps.location.pathname !== this.props.location.pathname) {
            this.fetchData();
        }
        if ((!this.canLoadEventEarly(prevProps) && !(prevState === null || prevState === void 0 ? void 0 : prevState.group) && this.state.group) ||
            (((_a = prevProps.params) === null || _a === void 0 ? void 0 : _a.eventId) !== ((_b = this.props.params) === null || _b === void 0 ? void 0 : _b.eventId) && this.state.group)) {
            this.getEvent(this.state.group);
        }
    };
    GroupDetails.prototype.componentWillUnmount = function () {
        groupStore_1.default.reset();
        callIfFunction_1.callIfFunction(this.listener);
        if (this.interval) {
            clearInterval(this.interval);
        }
    };
    Object.defineProperty(GroupDetails.prototype, "initialState", {
        get: function () {
            return {
                group: null,
                loading: true,
                loadingEvent: true,
                loadingGroup: true,
                error: false,
                eventError: false,
                errorType: null,
                project: null,
            };
        },
        enumerable: false,
        configurable: true
    });
    GroupDetails.prototype.canLoadEventEarly = function (props) {
        return !props.params.eventId || ['oldest', 'latest'].includes(props.params.eventId);
    };
    Object.defineProperty(GroupDetails.prototype, "groupDetailsEndpoint", {
        get: function () {
            return "/issues/" + this.props.params.groupId + "/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(GroupDetails.prototype, "groupReleaseEndpoint", {
        get: function () {
            return "/issues/" + this.props.params.groupId + "/first-last-release/";
        },
        enumerable: false,
        configurable: true
    });
    GroupDetails.prototype.getEvent = function (group) {
        var _a;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _b, params, environments, api, orgSlug, groupId, eventId, projectId, event_1, err_1;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (group) {
                            this.setState({ loadingEvent: true, eventError: false });
                        }
                        _b = this.props, params = _b.params, environments = _b.environments, api = _b.api;
                        orgSlug = params.orgId;
                        groupId = params.groupId;
                        eventId = (params === null || params === void 0 ? void 0 : params.eventId) || 'latest';
                        projectId = (_a = group === null || group === void 0 ? void 0 : group.project) === null || _a === void 0 ? void 0 : _a.slug;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, utils_1.fetchGroupEvent(api, orgSlug, groupId, eventId, environments, projectId)];
                    case 2:
                        event_1 = _c.sent();
                        this.setState({ event: event_1, loading: false, eventError: false, loadingEvent: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        // This is an expected error, capture to Sentry so that it is not considered as an unhandled error
                        Sentry.captureException(err_1);
                        this.setState({ eventError: true, loading: false, loadingEvent: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.getCurrentRouteInfo = function (group) {
        var _a = this.props, routes = _a.routes, organization = _a.organization;
        var event = this.state.event;
        // All the routes under /organizations/:orgId/issues/:groupId have a defined props
        var _b = routes[routes.length - 1].props, currentTab = _b.currentTab, isEventRoute = _b.isEventRoute;
        var baseUrl = isEventRoute && event
            ? "/organizations/" + organization.slug + "/issues/" + group.id + "/events/" + event.id + "/"
            : "/organizations/" + organization.slug + "/issues/" + group.id + "/";
        return { currentTab: currentTab, baseUrl: baseUrl };
    };
    GroupDetails.prototype.updateReprocessingProgress = function () {
        var hasReprocessingV2Feature = this.hasReprocessingV2Feature();
        if (!hasReprocessingV2Feature) {
            return;
        }
        this.interval = setInterval(this.refetchGroup, 30000);
    };
    GroupDetails.prototype.hasReprocessingV2Feature = function () {
        var _a;
        var organization = this.props.organization;
        return (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2');
    };
    GroupDetails.prototype.getReprocessingNewRoute = function (data) {
        var _a = this.props, routes = _a.routes, location = _a.location, params = _a.params;
        var groupId = params.groupId;
        var nextGroupId = data.id;
        var hasReprocessingV2Feature = this.hasReprocessingV2Feature();
        var reprocessingStatus = utils_1.getGroupReprocessingStatus(data);
        var _b = this.getCurrentRouteInfo(data), currentTab = _b.currentTab, baseUrl = _b.baseUrl;
        if (groupId !== nextGroupId) {
            if (hasReprocessingV2Feature) {
                // Redirects to the Activities tab
                if (reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                    currentTab !== header_1.TAB.ACTIVITY) {
                    return {
                        pathname: "" + baseUrl + header_1.TAB.ACTIVITY + "/",
                        query: tslib_1.__assign(tslib_1.__assign({}, params), { groupId: nextGroupId }),
                    };
                }
            }
            return recreateRoute_1.default('', {
                routes: routes,
                location: location,
                params: tslib_1.__assign(tslib_1.__assign({}, params), { groupId: nextGroupId }),
            });
        }
        if (hasReprocessingV2Feature) {
            if (reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSING &&
                currentTab !== header_1.TAB.DETAILS) {
                return {
                    pathname: baseUrl,
                    query: params,
                };
            }
            if (reprocessingStatus === utils_1.ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                currentTab !== header_1.TAB.ACTIVITY &&
                currentTab !== header_1.TAB.USER_FEEDBACK) {
                return {
                    pathname: "" + baseUrl + header_1.TAB.ACTIVITY + "/",
                    query: params,
                };
            }
        }
        return undefined;
    };
    GroupDetails.prototype.getGroupQuery = function () {
        var environments = this.props.environments;
        // Note, we do not want to include the environment key at all if there are no environments
        var query = tslib_1.__assign(tslib_1.__assign({}, (environments ? { environment: environments } : {})), { expand: 'inbox', collapse: 'release' });
        return query;
    };
    GroupDetails.prototype.getFetchDataRequestErrorType = function (status) {
        if (!status) {
            return null;
        }
        if (status === 404) {
            return constants_1.ERROR_TYPES.GROUP_NOT_FOUND;
        }
        if (status === 403) {
            return constants_1.ERROR_TYPES.MISSING_MEMBERSHIP;
        }
        return null;
    };
    GroupDetails.prototype.handleRequestError = function (error) {
        Sentry.captureException(error);
        var errorType = this.getFetchDataRequestErrorType(error === null || error === void 0 ? void 0 : error.status);
        this.setState({
            loadingGroup: false,
            loading: false,
            error: true,
            errorType: errorType,
        });
    };
    GroupDetails.prototype.fetchGroupReleases = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var api, releases;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        return [4 /*yield*/, api.requestPromise(this.groupReleaseEndpoint)];
                    case 1:
                        releases = _a.sent();
                        groupStore_1.default.onPopulateReleases(this.props.params.groupId, releases);
                        return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, isGlobalSelectionReady, params, eventPromise, groupPromise, _b, data, reprocessingNewRoute, project, locationWithProject, error_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, isGlobalSelectionReady = _a.isGlobalSelectionReady, params = _a.params;
                        // Need to wait for global selection store to be ready before making request
                        if (!isGlobalSelectionReady) {
                            return [2 /*return*/];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 4, , 5]);
                        eventPromise = this.canLoadEventEarly(this.props)
                            ? this.getEvent()
                            : undefined;
                        return [4 /*yield*/, api.requestPromise(this.groupDetailsEndpoint, {
                                query: this.getGroupQuery(),
                            })];
                    case 2:
                        groupPromise = _c.sent();
                        return [4 /*yield*/, Promise.all([groupPromise, eventPromise])];
                    case 3:
                        _b = tslib_1.__read.apply(void 0, [_c.sent(), 1]), data = _b[0];
                        this.fetchGroupReleases();
                        reprocessingNewRoute = this.getReprocessingNewRoute(data);
                        if (reprocessingNewRoute) {
                            ReactRouter.browserHistory.push(reprocessingNewRoute);
                            return [2 /*return*/];
                        }
                        project = data.project;
                        utils_1.markEventSeen(api, params.orgId, project.slug, params.groupId);
                        if (!project) {
                            Sentry.withScope(function () {
                                Sentry.captureException(new Error('Project not found'));
                            });
                        }
                        else {
                            locationWithProject = tslib_1.__assign({}, this.props.location);
                            if (locationWithProject.query.project === undefined &&
                                locationWithProject.query._allp === undefined) {
                                // We use _allp as a temporary measure to know they came from the
                                // issue list page with no project selected (all projects included in
                                // filter).
                                //
                                // If it is not defined, we add the locked project id to the URL
                                // (this is because if someone navigates directly to an issue on
                                // single-project priveleges, then goes back - they were getting
                                // assigned to the first project).
                                //
                                // If it is defined, we do not so that our back button will bring us
                                // to the issue list page with no project selected instead of the
                                // locked project.
                                locationWithProject.query.project = project.id;
                            }
                            // We delete _allp from the URL to keep the hack a bit cleaner, but
                            // this is not an ideal solution and will ultimately be replaced with
                            // something smarter.
                            delete locationWithProject.query._allp;
                            ReactRouter.browserHistory.replace(locationWithProject);
                        }
                        this.setState({ project: project, loadingGroup: false });
                        groupStore_1.default.loadInitialData([data]);
                        return [3 /*break*/, 5];
                    case 4:
                        error_2 = _c.sent();
                        this.handleRequestError(error_2);
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.onGroupChange = function (itemIds) {
        var id = this.props.params.groupId;
        if (itemIds.has(id)) {
            var group = groupStore_1.default.get(id);
            if (group) {
                // TODO(ts) This needs a better approach. issueActions is splicing attributes onto
                // group objects to cheat here.
                if (group.stale) {
                    this.fetchData();
                    return;
                }
                this.setState({
                    group: group,
                });
            }
        }
    };
    GroupDetails.prototype.getTitle = function () {
        var organization = this.props.organization;
        var group = this.state.group;
        var defaultTitle = 'Sentry';
        if (!group) {
            return defaultTitle;
        }
        var title = events_1.getTitle(group, organization === null || organization === void 0 ? void 0 : organization.features).title;
        var message = events_1.getMessage(group);
        var project = group.project;
        var eventDetails = organization.slug + " - " + project.slug;
        if (title && message) {
            return title + ": " + message + " - " + eventDetails;
        }
        return (title || message || defaultTitle) + " - " + eventDetails;
    };
    GroupDetails.prototype.renderError = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, location = _c.location;
        var projects = (_a = organization.projects) !== null && _a !== void 0 ? _a : [];
        var projectId = location.query.project;
        var projectSlug = (_b = projects.find(function (proj) { return proj.id === projectId; })) === null || _b === void 0 ? void 0 : _b.slug;
        switch (this.state.errorType) {
            case constants_1.ERROR_TYPES.GROUP_NOT_FOUND:
                return (<loadingError_1.default message={locale_1.t('The issue you were looking for was not found.')}/>);
            case constants_1.ERROR_TYPES.MISSING_MEMBERSHIP:
                return (<missingProjectMembership_1.default organization={this.props.organization} projectSlug={projectSlug}/>);
            default:
                return <loadingError_1.default onRetry={this.remountComponent}/>;
        }
    };
    GroupDetails.prototype.renderContent = function (project, group) {
        var _this = this;
        var _a = this.props, children = _a.children, environments = _a.environments;
        var _b = this.state, loadingEvent = _b.loadingEvent, eventError = _b.eventError, event = _b.event;
        var _c = this.getCurrentRouteInfo(group), currentTab = _c.currentTab, baseUrl = _c.baseUrl;
        var groupReprocessingStatus = utils_1.getGroupReprocessingStatus(group);
        var childProps = {
            environments: environments,
            group: group,
            project: project,
        };
        if (currentTab === header_1.TAB.DETAILS) {
            childProps = tslib_1.__assign(tslib_1.__assign({}, childProps), { event: event, loadingEvent: loadingEvent, eventError: eventError, groupReprocessingStatus: groupReprocessingStatus, onRetry: function () { return _this.remountComponent(); } });
        }
        if (currentTab === header_1.TAB.TAGS) {
            childProps = tslib_1.__assign(tslib_1.__assign({}, childProps), { event: event, baseUrl: baseUrl });
        }
        return (<React.Fragment>
        <header_1.default groupReprocessingStatus={groupReprocessingStatus} project={project} event={event} group={group} currentTab={currentTab} baseUrl={baseUrl}/>
        {React.isValidElement(children)
                ? React.cloneElement(children, childProps)
                : children}
      </React.Fragment>);
    };
    GroupDetails.prototype.renderPageContent = function () {
        var _this = this;
        var _a;
        var _b = this.state, isError = _b.error, group = _b.group, project = _b.project, loading = _b.loading;
        var isLoading = loading || (!group && !isError);
        if (isLoading) {
            return <loadingIndicator_1.default />;
        }
        if (isError) {
            return this.renderError();
        }
        var organization = this.props.organization;
        return (<projects_1.default orgId={organization.slug} slugs={[(_a = project === null || project === void 0 ? void 0 : project.slug) !== null && _a !== void 0 ? _a : '']} data-test-id="group-projects-container">
        {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
                return initiallyLoaded ? (fetchError ? (<loadingError_1.default message={locale_1.t('Error loading the specified project')}/>) : (
                // TODO(ts): Update renderContent function to deal with empty group
                _this.renderContent(projects[0], group))) : (<loadingIndicator_1.default />);
            }}
      </projects_1.default>);
    };
    GroupDetails.prototype.render = function () {
        var project = this.state.project;
        return (<react_document_title_1.default title={this.getTitle()}>
        <globalSelectionHeader_1.default skipLoadLastUsed forceProject={project} showDateSelector={false} shouldForceProject lockedMessageSubject={locale_1.t('issue')} showIssueStreamLink showProjectSettingsLink>
          <organization_1.PageContent>{this.renderPageContent()}</organization_1.PageContent>
        </globalSelectionHeader_1.default>
      </react_document_title_1.default>);
    };
    GroupDetails.childContextTypes = {
        group: sentryTypes_1.default.Group,
        location: prop_types_1.default.object,
    };
    return GroupDetails;
}(React.Component));
exports.default = withApi_1.default(Sentry.withProfiler(GroupDetails));
//# sourceMappingURL=groupDetails.jsx.map