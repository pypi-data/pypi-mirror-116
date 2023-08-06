Object.defineProperty(exports, "__esModule", { value: true });
exports.BorderlessEventEntries = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var contexts_1 = tslib_1.__importDefault(require("app/components/events/contexts"));
var contextSummary_1 = tslib_1.__importDefault(require("app/components/events/contextSummary/contextSummary"));
var device_1 = tslib_1.__importDefault(require("app/components/events/device"));
var errors_1 = tslib_1.__importDefault(require("app/components/events/errors"));
var eventAttachments_1 = tslib_1.__importDefault(require("app/components/events/eventAttachments"));
var eventCause_1 = tslib_1.__importDefault(require("app/components/events/eventCause"));
var eventCauseEmpty_1 = tslib_1.__importDefault(require("app/components/events/eventCauseEmpty"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var eventExtraData_1 = tslib_1.__importDefault(require("app/components/events/eventExtraData/eventExtraData"));
var eventSdk_1 = tslib_1.__importDefault(require("app/components/events/eventSdk"));
var eventTags_1 = tslib_1.__importDefault(require("app/components/events/eventTags/eventTags"));
var groupingInfo_1 = tslib_1.__importDefault(require("app/components/events/groupingInfo"));
var packageData_1 = tslib_1.__importDefault(require("app/components/events/packageData"));
var rrwebIntegration_1 = tslib_1.__importDefault(require("app/components/events/rrwebIntegration"));
var sdkUpdates_1 = tslib_1.__importDefault(require("app/components/events/sdkUpdates"));
var styles_1 = require("app/components/events/styles");
var userFeedback_1 = tslib_1.__importDefault(require("app/components/events/userFeedback"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var event_1 = require("app/types/event");
var utils_1 = require("app/types/utils");
var utils_2 = require("app/utils");
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var projectProcessingIssues_1 = require("app/views/settings/project/projectProcessingIssues");
var findBestThread_1 = tslib_1.__importDefault(require("./interfaces/threads/threadSelector/findBestThread"));
var getThreadException_1 = tslib_1.__importDefault(require("./interfaces/threads/threadSelector/getThreadException"));
var eventEntry_1 = tslib_1.__importDefault(require("./eventEntry"));
var eventTagsAndScreenshot_1 = tslib_1.__importDefault(require("./eventTagsAndScreenshot"));
var MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH = /^(([\w\$]\.[\w\$]{1,2})|([\w\$]{2}\.[\w\$]\.[\w\$]))(\.|$)/g;
var EventEntries = react_1.memo(function (_a) {
    var _b, _c;
    var organization = _a.organization, project = _a.project, location = _a.location, api = _a.api, event = _a.event, group = _a.group, className = _a.className, _d = _a.isShare, isShare = _d === void 0 ? false : _d, _e = _a.showExampleCommit, showExampleCommit = _e === void 0 ? false : _e, _f = _a.showTagSummary, showTagSummary = _f === void 0 ? true : _f, _g = _a.isBorderless, isBorderless = _g === void 0 ? false : _g;
    var _h = tslib_1.__read(react_1.useState(true), 2), isLoading = _h[0], setIsLoading = _h[1];
    var _j = tslib_1.__read(react_1.useState([]), 2), proGuardErrors = _j[0], setProGuardErrors = _j[1];
    var _k = tslib_1.__read(react_1.useState([]), 2), attachments = _k[0], setAttachments = _k[1];
    var orgSlug = organization.slug;
    var projectSlug = project.slug;
    var orgFeatures = (_b = organization === null || organization === void 0 ? void 0 : organization.features) !== null && _b !== void 0 ? _b : [];
    var hasEventAttachmentsFeature = orgFeatures.includes('event-attachments');
    react_1.useEffect(function () {
        checkProGuardError();
        recordIssueError();
        fetchAttachments();
    }, []);
    function recordIssueError() {
        if (!event || !event.errors || !(event.errors.length > 0)) {
            return;
        }
        var errors = event.errors;
        var errorTypes = errors.map(function (errorEntries) { return errorEntries.type; });
        var errorMessages = errors.map(function (errorEntries) { return errorEntries.message; });
        var orgId = organization.id;
        var platform = project.platform;
        analytics_1.analytics('issue_error_banner.viewed', tslib_1.__assign({ org_id: orgId ? parseInt(orgId, 10) : null, group: event === null || event === void 0 ? void 0 : event.groupID, error_type: errorTypes, error_message: errorMessages }, (platform && { platform: platform })));
    }
    function fetchProguardMappingFiles(query) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var proguardMappingFiles, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/files/dsyms/", {
                                method: 'GET',
                                query: {
                                    query: query,
                                    file_formats: 'proguard',
                                },
                            })];
                    case 1:
                        proguardMappingFiles = _a.sent();
                        return [2 /*return*/, proguardMappingFiles];
                    case 2:
                        error_1 = _a.sent();
                        Sentry.captureException(error_1);
                        // do nothing, the UI will not display extra error details
                        return [2 /*return*/, []];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function isDataMinified(str) {
        if (!str) {
            return false;
        }
        return !!tslib_1.__spreadArray([], tslib_1.__read(str.matchAll(MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH))).length;
    }
    function hasThreadOrExceptionMinifiedFrameData(definedEvent, bestThread) {
        var _a, _b, _c, _d, _e, _f, _g;
        if (!bestThread) {
            var exceptionValues = (_d = (_c = (_b = (_a = definedEvent.entries) === null || _a === void 0 ? void 0 : _a.find(function (e) { return e.type === event_1.EntryType.EXCEPTION; })) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.values) !== null && _d !== void 0 ? _d : [];
            return !!exceptionValues.find(function (exceptionValue) { var _a, _b; return (_b = (_a = exceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(function (frame) { return isDataMinified(frame.module); }); });
        }
        var threadExceptionValues = (_e = getThreadException_1.default(definedEvent, bestThread)) === null || _e === void 0 ? void 0 : _e.values;
        return !!(threadExceptionValues
            ? threadExceptionValues.find(function (threadExceptionValue) {
                var _a, _b;
                return (_b = (_a = threadExceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(function (frame) {
                    return isDataMinified(frame.module);
                });
            })
            : (_g = (_f = bestThread === null || bestThread === void 0 ? void 0 : bestThread.stacktrace) === null || _f === void 0 ? void 0 : _f.frames) === null || _g === void 0 ? void 0 : _g.find(function (frame) { return isDataMinified(frame.module); }));
    }
    function checkProGuardError() {
        var _a, _b, _c, _d, _e, _f, _g;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var hasEventErrorsProGuardMissingMapping, newProGuardErrors, debugImages, proGuardImage, proGuardImageUuid, proguardMappingFiles, threads, bestThread, hasThreadOrExceptionMinifiedData;
            return tslib_1.__generator(this, function (_h) {
                switch (_h.label) {
                    case 0:
                        if (!event || event.platform !== 'java') {
                            setIsLoading(false);
                            return [2 /*return*/];
                        }
                        hasEventErrorsProGuardMissingMapping = (_a = event.errors) === null || _a === void 0 ? void 0 : _a.find(function (error) { return error.type === 'proguard_missing_mapping'; });
                        if (hasEventErrorsProGuardMissingMapping) {
                            setIsLoading(false);
                            return [2 /*return*/];
                        }
                        newProGuardErrors = [];
                        debugImages = (_c = (_b = event.entries) === null || _b === void 0 ? void 0 : _b.find(function (e) { return e.type === event_1.EntryType.DEBUGMETA; })) === null || _c === void 0 ? void 0 : _c.data.images;
                        proGuardImage = debugImages === null || debugImages === void 0 ? void 0 : debugImages.find(function (debugImage) { return (debugImage === null || debugImage === void 0 ? void 0 : debugImage.type) === 'proguard'; });
                        proGuardImageUuid = proGuardImage === null || proGuardImage === void 0 ? void 0 : proGuardImage.uuid;
                        if (!utils_2.defined(proGuardImageUuid)) return [3 /*break*/, 2];
                        if (isShare) {
                            setIsLoading(false);
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, fetchProguardMappingFiles(proGuardImageUuid)];
                    case 1:
                        proguardMappingFiles = _h.sent();
                        if (!proguardMappingFiles.length) {
                            newProGuardErrors.push({
                                type: 'proguard_missing_mapping',
                                message: projectProcessingIssues_1.projectProcessingIssuesMessages.proguard_missing_mapping,
                                data: { mapping_uuid: proGuardImageUuid },
                            });
                        }
                        setProGuardErrors(newProGuardErrors);
                        setIsLoading(false);
                        return [2 /*return*/];
                    case 2:
                        if (proGuardImage) {
                            Sentry.withScope(function (s) {
                                s.setLevel(Sentry.Severity.Warning);
                                if (event.sdk) {
                                    s.setTag('offending.event.sdk.name', event.sdk.name);
                                    s.setTag('offending.event.sdk.version', event.sdk.version);
                                }
                                Sentry.captureMessage('Event contains proguard image but not uuid');
                            });
                        }
                        _h.label = 3;
                    case 3:
                        threads = (_g = (_f = (_e = (_d = event.entries) === null || _d === void 0 ? void 0 : _d.find(function (e) { return e.type === event_1.EntryType.THREADS; })) === null || _e === void 0 ? void 0 : _e.data) === null || _f === void 0 ? void 0 : _f.values) !== null && _g !== void 0 ? _g : [];
                        bestThread = findBestThread_1.default(threads);
                        hasThreadOrExceptionMinifiedData = hasThreadOrExceptionMinifiedFrameData(event, bestThread);
                        if (hasThreadOrExceptionMinifiedData) {
                            newProGuardErrors.push({
                                type: 'proguard_potentially_misconfigured_plugin',
                                message: locale_1.tct('Some frames appear to be minified. Did you configure the [plugin]?', {
                                    plugin: (<externalLink_1.default href="https://docs.sentry.io/platforms/android/proguard/#gradle">
                  Sentry Gradle Plugin
                </externalLink_1.default>),
                                }),
                            });
                            // This capture will be removed once we're confident with the level of effectiveness
                            Sentry.withScope(function (s) {
                                s.setLevel(Sentry.Severity.Warning);
                                if (event.sdk) {
                                    s.setTag('offending.event.sdk.name', event.sdk.name);
                                    s.setTag('offending.event.sdk.version', event.sdk.version);
                                }
                                Sentry.captureMessage(!proGuardImage
                                    ? 'No Proguard is used at all, but a frame did match the regex'
                                    : "Displaying ProGuard warning 'proguard_potentially_misconfigured_plugin' for suspected event");
                            });
                        }
                        setProGuardErrors(newProGuardErrors);
                        setIsLoading(false);
                        return [2 /*return*/];
                }
            });
        });
    }
    function fetchAttachments() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, error_2;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!event || isShare || !hasEventAttachmentsFeature) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/events/" + event.id + "/attachments/")];
                    case 2:
                        response = _a.sent();
                        setAttachments(response);
                        return [3 /*break*/, 4];
                    case 3:
                        error_2 = _a.sent();
                        Sentry.captureException(error_2);
                        indicator_1.addErrorMessage('An error occurred while fetching attachments');
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function renderEntries(definedEvent) {
        var entries = definedEvent.entries;
        if (!Array.isArray(entries)) {
            return null;
        }
        return entries.map(function (entry, entryIdx) { return (<errorBoundary_1.default key={"entry-" + entryIdx} customComponent={<eventDataSection_1.default type={entry.type} title={entry.type}>
              <p>{locale_1.t('There was an error rendering this data.')}</p>
            </eventDataSection_1.default>}>
          <eventEntry_1.default projectSlug={projectSlug} group={group} organization={organization} event={definedEvent} entry={entry}/>
        </errorBoundary_1.default>); });
    }
    function handleDeleteAttachment(attachmentId) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var error_3;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!event) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/events/" + event.id + "/attachments/" + attachmentId + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        setAttachments(attachments.filter(function (attachment) { return attachment.id !== attachmentId; }));
                        return [3 /*break*/, 4];
                    case 3:
                        error_3 = _a.sent();
                        Sentry.captureException(error_3);
                        indicator_1.addErrorMessage('An error occurred while deleteting the attachment');
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    if (!event) {
        return (<LatestEventNotAvailable>
          <h3>{locale_1.t('Latest Event Not Available')}</h3>
        </LatestEventNotAvailable>);
    }
    var hasQueryFeature = orgFeatures.includes('discover-query');
    var hasMobileScreenshotsFeature = orgFeatures.includes('mobile-screenshots');
    var hasContext = !utils_2.objectIsEmpty(event.user) || !utils_2.objectIsEmpty(event.contexts);
    var hasErrors = !utils_2.objectIsEmpty(event.errors) || !!proGuardErrors.length;
    return (<div className={className} data-test-id={"event-entries-loading-" + isLoading}>
        {hasErrors && !isLoading && (<errors_1.default event={event} orgSlug={orgSlug} projectSlug={projectSlug} proGuardErrors={proGuardErrors}/>)}
        {!isShare &&
            utils_1.isNotSharedOrganization(organization) &&
            (showExampleCommit ? (<eventCauseEmpty_1.default event={event} organization={organization} project={project}/>) : (<eventCause_1.default organization={organization} project={project} event={event} group={group}/>))}
        {event.userReport && group && (<StyledEventUserFeedback report={event.userReport} orgId={orgSlug} issueId={group.id} includeBorder={!hasErrors}/>)}
        {showTagSummary &&
            (hasMobileScreenshotsFeature ? (<eventTagsAndScreenshot_1.default event={event} organization={organization} projectId={projectSlug} location={location} hasQueryFeature={hasQueryFeature} isShare={isShare} hasContext={hasContext} isBorderless={isBorderless} attachments={attachments} onDeleteScreenshot={handleDeleteAttachment}/>) : ((!!((_c = event.tags) !== null && _c !== void 0 ? _c : []).length || hasContext) && (<StyledEventDataSection title={locale_1.t('Tags')} type="tags">
                {hasContext && <contextSummary_1.default event={event}/>}
                <eventTags_1.default event={event} organization={organization} projectId={projectSlug} location={location} hasQueryFeature={hasQueryFeature}/>
              </StyledEventDataSection>)))}
        {renderEntries(event)}
        {hasContext && <contexts_1.default group={group} event={event}/>}
        {event && !utils_2.objectIsEmpty(event.context) && <eventExtraData_1.default event={event}/>}
        {event && !utils_2.objectIsEmpty(event.packages) && <packageData_1.default event={event}/>}
        {event && !utils_2.objectIsEmpty(event.device) && <device_1.default event={event}/>}
        {!isShare && hasEventAttachmentsFeature && (<eventAttachments_1.default event={event} orgId={orgSlug} projectId={projectSlug} location={location} attachments={attachments} onDeleteAttachment={handleDeleteAttachment}/>)}
        {event.sdk && !utils_2.objectIsEmpty(event.sdk) && <eventSdk_1.default sdk={event.sdk}/>}
        {!isShare && (event === null || event === void 0 ? void 0 : event.sdkUpdates) && event.sdkUpdates.length > 0 && (<sdkUpdates_1.default event={tslib_1.__assign({ sdkUpdates: event.sdkUpdates }, event)}/>)}
        {!isShare && event.groupID && (<groupingInfo_1.default projectId={projectSlug} event={event} showGroupingConfig={orgFeatures.includes('set-grouping-config')}/>)}
        {!isShare && hasEventAttachmentsFeature && (<rrwebIntegration_1.default event={event} orgId={orgSlug} projectId={projectSlug}/>)}
      </div>);
});
var LatestEventNotAvailable = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n"], ["\n  padding: ", " ", ";\n"])), space_1.default(2), space_1.default(4));
var ErrorContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"], ["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"])));
var BorderlessEventEntries = styled_1.default(EventEntries)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  & ", " {\n    padding: ", " 0 0 0;\n  }\n  & ", ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & ", " {\n    margin-bottom: ", ";\n  }\n"], ["\n  & " /* sc-selector */, " {\n    padding: ", " 0 0 0;\n  }\n  & " /* sc-selector */, ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & " /* sc-selector */, " {\n    margin-bottom: ", ";\n  }\n"])), /* sc-selector */ styles_1.DataSection, space_1.default(3), /* sc-selector */ styles_1.DataSection, /* sc-selector */ ErrorContainer, space_1.default(2));
exports.BorderlessEventEntries = BorderlessEventEntries;
var StyledEventUserFeedback = styled_1.default(userFeedback_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  border-radius: 0;\n  box-shadow: none;\n  padding: ", " ", " 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"], ["\n  border-radius: 0;\n  box-shadow: none;\n  padding: ", " ", " 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"])), space_1.default(3), space_1.default(4), function (p) { return (p.includeBorder ? "border-top: 1px solid " + p.theme.innerBorder + ";" : ''); });
var StyledEventDataSection = styled_1.default(eventDataSection_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
// TODO(ts): any required due to our use of SharedViewOrganization
exports.default = withOrganization_1.default(withApi_1.default(EventEntries));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=eventEntries.jsx.map