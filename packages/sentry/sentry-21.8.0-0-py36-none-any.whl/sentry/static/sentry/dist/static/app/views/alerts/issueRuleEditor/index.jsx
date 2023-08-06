Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var indicator_1 = require("app/actionCreators/indicator");
var onboardingTasks_1 = require("app/actionCreators/onboardingTasks");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var loadingMask_1 = tslib_1.__importDefault(require("app/components/loadingMask"));
var panels_1 = require("app/components/panels");
var selectMembers_1 = tslib_1.__importDefault(require("app/components/selectMembers"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var analytics_1 = require("app/utils/analytics");
var environment_1 = require("app/utils/environment");
var isActiveSuperuser_1 = require("app/utils/isActiveSuperuser");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTeams_1 = tslib_1.__importDefault(require("app/utils/withTeams"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var ruleNodeList_1 = tslib_1.__importDefault(require("./ruleNodeList"));
var FREQUENCY_CHOICES = [
    ['5', locale_1.t('5 minutes')],
    ['10', locale_1.t('10 minutes')],
    ['30', locale_1.t('30 minutes')],
    ['60', locale_1.t('60 minutes')],
    ['180', locale_1.t('3 hours')],
    ['720', locale_1.t('12 hours')],
    ['1440', locale_1.t('24 hours')],
    ['10080', locale_1.t('one week')],
    ['43200', locale_1.t('30 days')],
];
var ACTION_MATCH_CHOICES = [
    ['all', locale_1.t('all')],
    ['any', locale_1.t('any')],
    ['none', locale_1.t('none')],
];
var ACTION_MATCH_CHOICES_MIGRATED = [
    ['all', locale_1.t('all')],
    ['any', locale_1.t('any')],
];
var defaultRule = {
    actionMatch: 'all',
    filterMatch: 'all',
    actions: [],
    conditions: [],
    filters: [],
    name: '',
    frequency: 30,
    environment: constants_1.ALL_ENVIRONMENTS_KEY,
};
var POLLING_MAX_TIME_LIMIT = 3 * 60000;
function isSavedAlertRule(rule) {
    var _a;
    return (_a = rule === null || rule === void 0 ? void 0 : rule.hasOwnProperty('id')) !== null && _a !== void 0 ? _a : false;
}
var IssueRuleEditor = /** @class */ (function (_super) {
    tslib_1.__extends(IssueRuleEditor, _super);
    function IssueRuleEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.pollHandler = function (quitTime) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, project, uuid, origRule, response, status_1, rule, error, ruleId, isNew, _b;
            var _this = this;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (Date.now() > quitTime) {
                            indicator_1.addErrorMessage(locale_1.t('Looking for that channel took too long :('));
                            this.setState({ loading: false });
                            return [2 /*return*/];
                        }
                        _a = this.props, organization = _a.organization, project = _a.project;
                        uuid = this.state.uuid;
                        origRule = this.state.rule;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/rule-task/" + uuid + "/")];
                    case 2:
                        response = _c.sent();
                        status_1 = response.status, rule = response.rule, error = response.error;
                        if (status_1 === 'pending') {
                            setTimeout(function () {
                                _this.pollHandler(quitTime);
                            }, 1000);
                            return [2 /*return*/];
                        }
                        if (status_1 === 'failed') {
                            this.setState({
                                detailedError: { actions: [error ? error : locale_1.t('An error occurred')] },
                                loading: false,
                            });
                            this.handleRuleSaveFailure(locale_1.t('An error occurred'));
                        }
                        if (rule) {
                            ruleId = isSavedAlertRule(origRule) ? origRule.id + "/" : '';
                            isNew = !ruleId;
                            this.handleRuleSuccess(isNew, rule);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.handleRuleSaveFailure(locale_1.t('An error occurred'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleRuleSuccess = function (isNew, rule) {
            var _a = _this.props, organization = _a.organization, router = _a.router;
            _this.setState({ detailedError: null, loading: false, rule: rule });
            // The onboarding task will be completed on the server side when the alert
            // is created
            onboardingTasks_1.updateOnboardingTask(null, organization, {
                task: types_1.OnboardingTaskKey.ALERT_RULE,
                status: 'complete',
            });
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
            router.push("/organizations/" + organization.slug + "/alerts/rules/");
            indicator_1.addSuccessMessage(isNew ? locale_1.t('Created alert rule') : locale_1.t('Updated alert rule'));
        };
        _this.handleSubmit = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var rule, ruleId, isNew, _a, project, organization, endpoint, transaction, _b, _c, action, splitActionId, actionName, _d, data, resp, err_1;
            var e_1, _e;
            return tslib_1.__generator(this, function (_f) {
                switch (_f.label) {
                    case 0:
                        rule = this.state.rule;
                        ruleId = isSavedAlertRule(rule) ? rule.id + "/" : '';
                        isNew = !ruleId;
                        _a = this.props, project = _a.project, organization = _a.organization;
                        endpoint = "/projects/" + organization.slug + "/" + project.slug + "/rules/" + ruleId;
                        if (rule && rule.environment === constants_1.ALL_ENVIRONMENTS_KEY) {
                            delete rule.environment;
                        }
                        indicator_1.addLoadingMessage();
                        _f.label = 1;
                    case 1:
                        _f.trys.push([1, 3, , 4]);
                        transaction = analytics_1.metric.startTransaction({ name: 'saveAlertRule' });
                        transaction.setTag('type', 'issue');
                        transaction.setTag('operation', isNew ? 'create' : 'edit');
                        if (rule) {
                            try {
                                for (_b = tslib_1.__values(rule.actions), _c = _b.next(); !_c.done; _c = _b.next()) {
                                    action = _c.value;
                                    splitActionId = action.id.split('.');
                                    actionName = splitActionId[splitActionId.length - 1];
                                    if (actionName === 'SlackNotifyServiceAction') {
                                        transaction.setTag(actionName, true);
                                    }
                                }
                            }
                            catch (e_1_1) { e_1 = { error: e_1_1 }; }
                            finally {
                                try {
                                    if (_c && !_c.done && (_e = _b.return)) _e.call(_b);
                                }
                                finally { if (e_1) throw e_1.error; }
                            }
                            transaction.setData('actions', rule.actions);
                        }
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                includeAllArgs: true,
                                method: isNew ? 'POST' : 'PUT',
                                data: rule,
                            })];
                    case 2:
                        _d = tslib_1.__read.apply(void 0, [_f.sent(), 3]), data = _d[0], resp = _d[2];
                        // if we get a 202 back it means that we have an async task
                        // running to lookup and verify the channel id for Slack.
                        if ((resp === null || resp === void 0 ? void 0 : resp.status) === 202) {
                            this.setState({ detailedError: null, loading: true, uuid: data.uuid });
                            this.fetchStatus();
                            indicator_1.addLoadingMessage(locale_1.t('Looking through all your channels...'));
                        }
                        else {
                            this.handleRuleSuccess(isNew, data);
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _f.sent();
                        this.setState({
                            detailedError: err_1.responseJSON || { __all__: 'Unknown error' },
                            loading: false,
                        });
                        this.handleRuleSaveFailure(locale_1.t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleDeleteRule = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var rule, ruleId, isNew, _a, project, organization, endpoint, err_2;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        rule = this.state.rule;
                        ruleId = isSavedAlertRule(rule) ? rule.id + "/" : '';
                        isNew = !ruleId;
                        _a = this.props, project = _a.project, organization = _a.organization;
                        if (isNew) {
                            return [2 /*return*/];
                        }
                        endpoint = "/projects/" + organization.slug + "/" + project.slug + "/rules/" + ruleId;
                        indicator_1.addLoadingMessage(locale_1.t('Deleting...'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Deleted alert rule'));
                        react_router_1.browserHistory.replace(recreateRoute_1.default('', tslib_1.__assign(tslib_1.__assign({}, this.props), { stepBack: -2 })));
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _b.sent();
                        this.setState({
                            detailedError: err_2.responseJSON || { __all__: 'Unknown error' },
                        });
                        indicator_1.addErrorMessage(locale_1.t('There was a problem deleting the alert'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleCancel = function () {
            var _a = _this.props, organization = _a.organization, router = _a.router;
            router.push("/organizations/" + organization.slug + "/alerts/rules/");
        };
        _this.hasError = function (field) {
            var detailedError = _this.state.detailedError;
            if (!detailedError) {
                return false;
            }
            return detailedError.hasOwnProperty(field);
        };
        _this.handleEnvironmentChange = function (val) {
            // If 'All Environments' is selected the value should be null
            if (val === constants_1.ALL_ENVIRONMENTS_KEY) {
                _this.handleChange('environment', null);
            }
            else {
                _this.handleChange('environment', val);
            }
        };
        _this.handleChange = function (prop, val) {
            _this.setState(function (prevState) {
                var clonedState = cloneDeep_1.default(prevState);
                set_1.default(clonedState, "rule[" + prop + "]", val);
                return tslib_1.__assign(tslib_1.__assign({}, clonedState), { detailedError: omit_1.default(prevState.detailedError, prop) });
            });
        };
        _this.handlePropertyChange = function (type, idx, prop, val) {
            _this.setState(function (prevState) {
                var clonedState = cloneDeep_1.default(prevState);
                set_1.default(clonedState, "rule[" + type + "][" + idx + "][" + prop + "]", val);
                return clonedState;
            });
        };
        _this.getInitialValue = function (type, id) {
            var _a, _b;
            var configuration = (_b = (_a = _this.state.configs) === null || _a === void 0 ? void 0 : _a[type]) === null || _b === void 0 ? void 0 : _b.find(function (c) { return c.id === id; });
            return (configuration === null || configuration === void 0 ? void 0 : configuration.formFields)
                ? Object.fromEntries(Object.entries(configuration.formFields)
                    // TODO(ts): Doesn't work if I cast formField as IssueAlertRuleFormField
                    .map(function (_a) {
                    var _b, _c, _d;
                    var _e = tslib_1.__read(_a, 2), key = _e[0], formField = _e[1];
                    return [
                        key,
                        (_b = formField === null || formField === void 0 ? void 0 : formField.initial) !== null && _b !== void 0 ? _b : (_d = (_c = formField === null || formField === void 0 ? void 0 : formField.choices) === null || _c === void 0 ? void 0 : _c[0]) === null || _d === void 0 ? void 0 : _d[0],
                    ];
                })
                    .filter(function (_a) {
                    var _b = tslib_1.__read(_a, 2), initial = _b[1];
                    return !!initial;
                }))
                : {};
        };
        _this.handleResetRow = function (type, idx, prop, val) {
            _this.setState(function (prevState) {
                var _a;
                var clonedState = cloneDeep_1.default(prevState);
                // Set initial configuration, but also set
                var id = clonedState.rule[type][idx].id;
                var newRule = tslib_1.__assign(tslib_1.__assign({}, _this.getInitialValue(type, id)), (_a = { id: id }, _a[prop] = val, _a));
                set_1.default(clonedState, "rule[" + type + "][" + idx + "]", newRule);
                return clonedState;
            });
        };
        _this.handleAddRow = function (type, id) {
            _this.setState(function (prevState) {
                var clonedState = cloneDeep_1.default(prevState);
                // Set initial configuration
                var newRule = tslib_1.__assign(tslib_1.__assign({}, _this.getInitialValue(type, id)), { id: id });
                var newTypeList = prevState.rule ? prevState.rule[type] : [];
                set_1.default(clonedState, "rule[" + type + "]", tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(newTypeList)), [newRule]));
                return clonedState;
            });
            var _a = _this.props, organization = _a.organization, project = _a.project;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'edit_alert_rule.add_row',
                eventName: 'Edit Alert Rule: Add Row',
                organization_id: organization.id,
                project_id: project.id,
                type: type,
                name: id,
            });
        };
        _this.handleDeleteRow = function (type, idx) {
            _this.setState(function (prevState) {
                var clonedState = cloneDeep_1.default(prevState);
                var newTypeList = prevState.rule ? prevState.rule[type] : [];
                if (prevState.rule) {
                    newTypeList.splice(idx, 1);
                }
                set_1.default(clonedState, "rule[" + type + "]", newTypeList);
                return clonedState;
            });
        };
        _this.handleAddCondition = function (id) { return _this.handleAddRow('conditions', id); };
        _this.handleAddAction = function (id) { return _this.handleAddRow('actions', id); };
        _this.handleAddFilter = function (id) { return _this.handleAddRow('filters', id); };
        _this.handleDeleteCondition = function (ruleIndex) {
            return _this.handleDeleteRow('conditions', ruleIndex);
        };
        _this.handleDeleteAction = function (ruleIndex) { return _this.handleDeleteRow('actions', ruleIndex); };
        _this.handleDeleteFilter = function (ruleIndex) { return _this.handleDeleteRow('filters', ruleIndex); };
        _this.handleChangeConditionProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('conditions', ruleIndex, prop, val);
        };
        _this.handleChangeActionProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('actions', ruleIndex, prop, val);
        };
        _this.handleChangeFilterProperty = function (ruleIndex, prop, val) {
            return _this.handlePropertyChange('filters', ruleIndex, prop, val);
        };
        _this.handleResetCondition = function (ruleIndex, prop, value) {
            return _this.handleResetRow('conditions', ruleIndex, prop, value);
        };
        _this.handleResetAction = function (ruleIndex, prop, value) {
            return _this.handleResetRow('actions', ruleIndex, prop, value);
        };
        _this.handleResetFilter = function (ruleIndex, prop, value) {
            return _this.handleResetRow('filters', ruleIndex, prop, value);
        };
        _this.handleValidateRuleName = function () {
            var _a;
            var isRuleNameEmpty = !((_a = _this.state.rule) === null || _a === void 0 ? void 0 : _a.name.trim());
            if (!isRuleNameEmpty) {
                return;
            }
            _this.setState(function (prevState) { return ({
                detailedError: tslib_1.__assign(tslib_1.__assign({}, prevState.detailedError), { name: [locale_1.t('Field Required')] }),
            }); });
        };
        _this.getTeamId = function () {
            var rule = _this.state.rule;
            var owner = rule === null || rule === void 0 ? void 0 : rule.owner;
            // ownership follows the format team:<id>, just grab the id
            return owner && owner.split(':')[1];
        };
        _this.handleOwnerChange = function (_a) {
            var value = _a.value;
            var ownerValue = value && "team:" + value;
            _this.handleChange('owner', ownerValue);
        };
        return _this;
    }
    IssueRuleEditor.prototype.getTitle = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var rule = this.state.rule;
        var ruleName = rule === null || rule === void 0 ? void 0 : rule.name;
        return routeTitle_1.default(ruleName ? locale_1.t('Alert %s', ruleName) : '', organization.slug, false, project === null || project === void 0 ? void 0 : project.slug);
    };
    IssueRuleEditor.prototype.getDefaultState = function () {
        var _a;
        var _b = this.props, teams = _b.teams, project = _b.project;
        var defaultState = tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { configs: null, detailedError: null, rule: tslib_1.__assign({}, defaultRule), environments: [], uuid: null });
        var projectTeamIds = new Set(project.teams.map(function (_a) {
            var id = _a.id;
            return id;
        }));
        var userTeam = (_a = teams.find(function (_a) {
            var isMember = _a.isMember, id = _a.id;
            return !!isMember && projectTeamIds.has(id);
        })) !== null && _a !== void 0 ? _a : null;
        defaultState.rule.owner = userTeam && "team:" + userTeam.id;
        return defaultState;
    };
    IssueRuleEditor.prototype.getEndpoints = function () {
        var _a = this.props.params, ruleId = _a.ruleId, projectId = _a.projectId, orgId = _a.orgId;
        var endpoints = [
            ['environments', "/projects/" + orgId + "/" + projectId + "/environments/"],
            ['configs', "/projects/" + orgId + "/" + projectId + "/rules/configuration/"],
        ];
        if (ruleId) {
            endpoints.push(['rule', "/projects/" + orgId + "/" + projectId + "/rules/" + ruleId + "/"]);
        }
        return endpoints;
    };
    IssueRuleEditor.prototype.onRequestSuccess = function (_a) {
        var _b, _c;
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey === 'rule' && data.name) {
            (_c = (_b = this.props).onChangeTitle) === null || _c === void 0 ? void 0 : _c.call(_b, data.name);
        }
    };
    IssueRuleEditor.prototype.fetchStatus = function () {
        var _this = this;
        // pollHandler calls itself until it gets either a success
        // or failed status but we don't want to poll forever so we pass
        // in a hard stop time of 3 minutes before we bail.
        var quitTime = Date.now() + POLLING_MAX_TIME_LIMIT;
        setTimeout(function () {
            _this.pollHandler(quitTime);
        }, 1000);
    };
    IssueRuleEditor.prototype.handleRuleSaveFailure = function (msg) {
        indicator_1.addErrorMessage(msg);
        analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
    };
    IssueRuleEditor.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IssueRuleEditor.prototype.renderError = function () {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {locale_1.t('Unable to access this alert rule -- check to make sure you have the correct permissions')}
      </alert_1.default>);
    };
    IssueRuleEditor.prototype.renderBody = function () {
        var _this = this;
        var _a, _b;
        var _c = this.props, project = _c.project, organization = _c.organization, teams = _c.teams;
        var environments = this.state.environments;
        var environmentChoices = tslib_1.__spreadArray([
            [constants_1.ALL_ENVIRONMENTS_KEY, locale_1.t('All Environments')]
        ], tslib_1.__read(((_a = environments === null || environments === void 0 ? void 0 : environments.map(function (env) { return [env.name, environment_1.getDisplayName(env)]; })) !== null && _a !== void 0 ? _a : [])));
        var _d = this.state, rule = _d.rule, detailedError = _d.detailedError;
        var _e = rule || {}, actions = _e.actions, filters = _e.filters, conditions = _e.conditions, frequency = _e.frequency, name = _e.name;
        var environment = !rule || !rule.environment ? constants_1.ALL_ENVIRONMENTS_KEY : rule.environment;
        var userTeams = teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        });
        var ownerId = (_b = rule === null || rule === void 0 ? void 0 : rule.owner) === null || _b === void 0 ? void 0 : _b.split(':')[1];
        // check if superuser or if user is on the alert's team
        var canEdit = isActiveSuperuser_1.isActiveSuperuser() || (ownerId ? userTeams.includes(ownerId) : true);
        var filteredTeamIds = new Set(userTeams);
        if (ownerId) {
            filteredTeamIds.add(ownerId);
        }
        // Note `key` on `<Form>` below is so that on initial load, we show
        // the form with a loading mask on top of it, but force a re-render by using
        // a different key when we have fetched the rule so that form inputs are filled in
        return (<access_1.default access={['alerts:write']}>
        {function (_a) {
                var _b, _c, _d, _e, _f;
                var hasAccess = _a.hasAccess;
                return (<StyledForm key={isSavedAlertRule(rule) ? rule.id : undefined} onCancel={_this.handleCancel} onSubmit={_this.handleSubmit} initialData={tslib_1.__assign(tslib_1.__assign({}, rule), { environment: environment, frequency: "" + frequency })} submitDisabled={!hasAccess || !canEdit} submitLabel={isSavedAlertRule(rule) ? locale_1.t('Save Rule') : locale_1.t('Save Rule')} extraButton={isSavedAlertRule(rule) ? (<confirm_1.default disabled={!hasAccess || !canEdit} priority="danger" confirmText={locale_1.t('Delete Rule')} onConfirm={_this.handleDeleteRule} header={locale_1.t('Delete Rule')} message={locale_1.t('Are you sure you want to delete this rule?')}>
                  <button_1.default priority="danger" type="button">
                    {locale_1.t('Delete Rule')}
                  </button_1.default>
                </confirm_1.default>) : null}>
            <list_1.default symbol="colored-numeric">
              {_this.state.loading && <SemiTransparentLoadingMask />}
              <StyledListItem>{locale_1.t('Add alert settings')}</StyledListItem>
              <panels_1.Panel>
                <panels_1.PanelBody>
                  <selectField_1.default className={classnames_1.default({
                        error: _this.hasError('environment'),
                    })} label={locale_1.t('Environment')} help={locale_1.t('Choose an environment for these conditions to apply to')} placeholder={locale_1.t('Select an Environment')} clearable={false} name="environment" choices={environmentChoices} onChange={function (val) { return _this.handleEnvironmentChange(val); }} disabled={!hasAccess || !canEdit}/>

                  <StyledField label={locale_1.t('Team')} help={locale_1.t('The team that can edit this alert.')} disabled={!hasAccess || !canEdit}>
                    <selectMembers_1.default showTeam project={project} organization={organization} value={_this.getTeamId()} onChange={_this.handleOwnerChange} filteredTeamIds={filteredTeamIds} includeUnassigned disabled={!hasAccess || !canEdit}/>
                  </StyledField>

                  <StyledField label={locale_1.t('Alert name')} help={locale_1.t('Add a name for this alert')} error={(_b = detailedError === null || detailedError === void 0 ? void 0 : detailedError.name) === null || _b === void 0 ? void 0 : _b[0]} disabled={!hasAccess || !canEdit} required stacked>
                    <input_1.default type="text" name="name" value={name} placeholder={locale_1.t('My Rule Name')} onChange={function (event) {
                        return _this.handleChange('name', event.target.value);
                    }} onBlur={_this.handleValidateRuleName} disabled={!hasAccess || !canEdit}/>
                  </StyledField>
                </panels_1.PanelBody>
              </panels_1.Panel>
              <StyledListItem>{locale_1.t('Set conditions')}</StyledListItem>
              <ConditionsPanel>
                <panels_1.PanelBody>
                  <Step>
                    <StepConnector />

                    <StepContainer>
                      <ChevronContainer>
                        <icons_1.IconChevron color="gray200" isCircled direction="right" size="sm"/>
                      </ChevronContainer>

                      <feature_1.default features={['projects:alert-filters']} project={project}>
                        {function (_a) {
                        var _b, _c;
                        var hasFeature = _a.hasFeature;
                        return (<StepContent>
                            <StepLead>
                              {locale_1.tct('[when:When] an event is captured by Sentry and [selector] of the following happens', {
                                when: <Badge />,
                                selector: (<EmbeddedWrapper>
                                      <EmbeddedSelectField className={classnames_1.default({
                                        error: _this.hasError('actionMatch'),
                                    })} inline={false} styles={{
                                        control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { minHeight: '20px', height: '20px' })); },
                                    }} isSearchable={false} isClearable={false} name="actionMatch" required flexibleControlStateSize choices={hasFeature
                                        ? ACTION_MATCH_CHOICES_MIGRATED
                                        : ACTION_MATCH_CHOICES} onChange={function (val) {
                                        return _this.handleChange('actionMatch', val);
                                    }} disabled={!hasAccess || !canEdit}/>
                                    </EmbeddedWrapper>),
                            })}
                            </StepLead>
                            <ruleNodeList_1.default nodes={(_c = (_b = _this.state.configs) === null || _b === void 0 ? void 0 : _b.conditions) !== null && _c !== void 0 ? _c : null} items={conditions !== null && conditions !== void 0 ? conditions : []} placeholder={hasFeature
                                ? locale_1.t('Add optional trigger...')
                                : locale_1.t('Add optional condition...')} onPropertyChange={_this.handleChangeConditionProperty} onAddRow={_this.handleAddCondition} onResetRow={_this.handleResetCondition} onDeleteRow={_this.handleDeleteCondition} organization={organization} project={project} disabled={!hasAccess || !canEdit} error={_this.hasError('conditions') && (<StyledAlert type="error">
                                    {detailedError === null || detailedError === void 0 ? void 0 : detailedError.conditions[0]}
                                  </StyledAlert>)}/>
                          </StepContent>);
                    }}
                      </feature_1.default>
                    </StepContainer>
                  </Step>

                  <feature_1.default features={['organizations:alert-filters', 'projects:alert-filters']} organization={organization} project={project} requireAll={false}>
                    <Step>
                      <StepConnector />

                      <StepContainer>
                        <ChevronContainer>
                          <icons_1.IconChevron color="gray200" isCircled direction="right" size="sm"/>
                        </ChevronContainer>

                        <StepContent>
                          <StepLead>
                            {locale_1.tct('[if:If] [selector] of these filters match', {
                        if: <Badge />,
                        selector: (<EmbeddedWrapper>
                                  <EmbeddedSelectField className={classnames_1.default({
                                error: _this.hasError('filterMatch'),
                            })} inline={false} styles={{
                                control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { minHeight: '20px', height: '20px' })); },
                            }} isSearchable={false} isClearable={false} name="filterMatch" required flexibleControlStateSize choices={ACTION_MATCH_CHOICES} onChange={function (val) {
                                return _this.handleChange('filterMatch', val);
                            }} disabled={!hasAccess || !canEdit}/>
                                </EmbeddedWrapper>),
                    })}
                          </StepLead>
                          <ruleNodeList_1.default nodes={(_d = (_c = _this.state.configs) === null || _c === void 0 ? void 0 : _c.filters) !== null && _d !== void 0 ? _d : null} items={filters !== null && filters !== void 0 ? filters : []} placeholder={locale_1.t('Add optional filter...')} onPropertyChange={_this.handleChangeFilterProperty} onAddRow={_this.handleAddFilter} onResetRow={_this.handleResetFilter} onDeleteRow={_this.handleDeleteFilter} organization={organization} project={project} disabled={!hasAccess || !canEdit} error={_this.hasError('filters') && (<StyledAlert type="error">
                                  {detailedError === null || detailedError === void 0 ? void 0 : detailedError.filters[0]}
                                </StyledAlert>)}/>
                        </StepContent>
                      </StepContainer>
                    </Step>
                  </feature_1.default>

                  <Step>
                    <StepContainer>
                      <ChevronContainer>
                        <icons_1.IconChevron isCircled color="gray200" direction="right" size="sm"/>
                      </ChevronContainer>
                      <StepContent>
                        <StepLead>
                          {locale_1.tct('[then:Then] perform these actions', {
                        then: <Badge />,
                    })}
                        </StepLead>

                        <ruleNodeList_1.default nodes={(_f = (_e = _this.state.configs) === null || _e === void 0 ? void 0 : _e.actions) !== null && _f !== void 0 ? _f : null} selectType="grouped" items={actions !== null && actions !== void 0 ? actions : []} placeholder={locale_1.t('Add action...')} onPropertyChange={_this.handleChangeActionProperty} onAddRow={_this.handleAddAction} onResetRow={_this.handleResetAction} onDeleteRow={_this.handleDeleteAction} organization={organization} project={project} disabled={!hasAccess || !canEdit} error={_this.hasError('actions') && (<StyledAlert type="error">
                                {detailedError === null || detailedError === void 0 ? void 0 : detailedError.actions[0]}
                              </StyledAlert>)}/>
                      </StepContent>
                    </StepContainer>
                  </Step>
                </panels_1.PanelBody>
              </ConditionsPanel>
              <StyledListItem>{locale_1.t('Set action interval')}</StyledListItem>
              <panels_1.Panel>
                <panels_1.PanelBody>
                  <selectField_1.default label={locale_1.t('Action Interval')} help={locale_1.t('Perform these actions once this often for an issue')} clearable={false} name="frequency" className={_this.hasError('frequency') ? ' error' : ''} value={frequency} required choices={FREQUENCY_CHOICES} onChange={function (val) { return _this.handleChange('frequency', val); }} disabled={!hasAccess || !canEdit}/>
                </panels_1.PanelBody>
              </panels_1.Panel>
            </list_1.default>
          </StyledForm>);
            }}
      </access_1.default>);
    };
    return IssueRuleEditor;
}(asyncView_1.default));
exports.default = withOrganization_1.default(withTeams_1.default(IssueRuleEditor));
// TODO(ts): Understand why styled is not correctly inheriting props here
var StyledForm = styled_1.default(form_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ConditionsPanel = styled_1.default(panels_1.Panel)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n  padding-bottom: ", ";\n"], ["\n  padding-top: ", ";\n  padding-bottom: ", ";\n"])), space_1.default(0.5), space_1.default(2));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var StyledListItem = styled_1.default(listItem_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: ", " 0 ", " 0;\n  font-size: ", ";\n"], ["\n  margin: ", " 0 ", " 0;\n  font-size: ", ";\n"])), space_1.default(2), space_1.default(1), function (p) { return p.theme.fontSizeExtraLarge; });
var Step = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  margin: ", " ", " ", " ", ";\n"], ["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  margin: ", " ", " ", " ", ";\n"])), space_1.default(4), space_1.default(4), space_1.default(3), space_1.default(1));
var StepContainer = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  flex-grow: 1;\n"], ["\n  position: relative;\n  display: flex;\n  align-items: flex-start;\n  flex-grow: 1;\n"])));
var StepContent = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StepConnector = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  height: 100%;\n  top: 28px;\n  left: 19px;\n  border-right: 1px ", " dashed;\n"], ["\n  position: absolute;\n  height: 100%;\n  top: 28px;\n  left: 19px;\n  border-right: 1px ", " dashed;\n"])), function (p) { return p.theme.gray300; });
var StepLead = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(0.5));
var ChevronContainer = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", " ", ";\n"])), space_1.default(0.5), space_1.default(1.5));
var Badge = styled_1.default('span')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  min-width: 56px;\n  background-color: ", ";\n  padding: 0 ", ";\n  border-radius: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  text-align: center;\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1.5;\n"], ["\n  display: inline-block;\n  min-width: 56px;\n  background-color: ", ";\n  padding: 0 ", ";\n  border-radius: ", ";\n  color: ", ";\n  text-transform: uppercase;\n  text-align: center;\n  font-size: ", ";\n  font-weight: 600;\n  line-height: 1.5;\n"])), function (p) { return p.theme.purple300; }, space_1.default(0.75), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.white; }, function (p) { return p.theme.fontSizeMedium; });
var EmbeddedWrapper = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin: 0 ", ";\n  width: 80px;\n"], ["\n  display: inline-block;\n  margin: 0 ", ";\n  width: 80px;\n"])), space_1.default(0.5));
var EmbeddedSelectField = styled_1.default(selectField_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n  font-weight: normal;\n  text-transform: none;\n"], ["\n  padding: 0;\n  font-weight: normal;\n  text-transform: none;\n"])));
var SemiTransparentLoadingMask = styled_1.default(loadingMask_1.default)(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  opacity: 0.6;\n  z-index: 1; /* Needed so that it sits above form elements */\n"], ["\n  opacity: 0.6;\n  z-index: 1; /* Needed so that it sits above form elements */\n"])));
var StyledField = styled_1.default(field_1.default)(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  :last-child {\n    padding-bottom: ", ";\n  }\n"], ["\n  :last-child {\n    padding-bottom: ", ";\n  }\n"])), space_1.default(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=index.jsx.map