Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var guideActions_1 = tslib_1.__importDefault(require("app/actions/guideActions"));
var organizationsActions_1 = tslib_1.__importDefault(require("app/actions/organizationsActions"));
var api_1 = require("app/api");
var getGuidesContent_1 = tslib_1.__importDefault(require("app/components/assistant/getGuidesContent"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var analytics_1 = require("app/utils/analytics");
function guidePrioritySort(a, b) {
    var _a, _b;
    var a_priority = (_a = a.priority) !== null && _a !== void 0 ? _a : Number.MAX_SAFE_INTEGER;
    var b_priority = (_b = b.priority) !== null && _b !== void 0 ? _b : Number.MAX_SAFE_INTEGER;
    if (a_priority === b_priority) {
        return a.guide.localeCompare(b.guide);
    }
    // lower number takes priority
    return a_priority - b_priority;
}
var defaultState = {
    guides: [],
    anchors: new Set(),
    currentGuide: null,
    currentStep: 0,
    orgId: null,
    orgSlug: null,
    forceShow: false,
    prevGuide: null,
};
var guideStoreConfig = {
    state: defaultState,
    init: function () {
        var _this = this;
        this.state = defaultState;
        this.api = new api_1.Client();
        this.listenTo(guideActions_1.default.fetchSucceeded, this.onFetchSucceeded);
        this.listenTo(guideActions_1.default.closeGuide, this.onCloseGuide);
        this.listenTo(guideActions_1.default.nextStep, this.onNextStep);
        this.listenTo(guideActions_1.default.toStep, this.onToStep);
        this.listenTo(guideActions_1.default.registerAnchor, this.onRegisterAnchor);
        this.listenTo(guideActions_1.default.unregisterAnchor, this.onUnregisterAnchor);
        this.listenTo(organizationsActions_1.default.setActive, this.onSetActiveOrganization);
        window.addEventListener('load', this.onURLChange, false);
        react_router_1.browserHistory.listen(function () { return _this.onURLChange(); });
    },
    onURLChange: function () {
        this.state.forceShow = window.location.hash === '#assistant';
        this.updateCurrentGuide();
    },
    onSetActiveOrganization: function (data) {
        this.state.orgId = data ? data.id : null;
        this.state.orgSlug = data ? data.slug : null;
        this.updateCurrentGuide();
    },
    onFetchSucceeded: function (data) {
        // It's possible we can get empty responses (seems to be Firefox specific)
        // Do nothing if `data` is empty
        // also, temporarily check data is in the correct format from the updated
        // assistant endpoint
        if (!data || !Array.isArray(data)) {
            return;
        }
        var guidesContent = getGuidesContent_1.default(this.state.orgSlug);
        // map server guide state (i.e. seen status) with guide content
        var guides = guidesContent.reduce(function (acc, content) {
            var serverGuide = data.find(function (guide) { return guide.guide === content.guide; });
            serverGuide &&
                acc.push(tslib_1.__assign(tslib_1.__assign({}, content), serverGuide));
            return acc;
        }, []);
        this.state.guides = guides;
        this.updateCurrentGuide();
    },
    onCloseGuide: function (dismissed) {
        var _a = this.state, currentGuide = _a.currentGuide, guides = _a.guides;
        // update the current guide seen to true or all guides
        // if markOthersAsSeen is true and the user is dismissing
        guides
            .filter(function (guide) {
            return guide.guide === (currentGuide === null || currentGuide === void 0 ? void 0 : currentGuide.guide) ||
                ((currentGuide === null || currentGuide === void 0 ? void 0 : currentGuide.markOthersAsSeen) && dismissed);
        })
            .forEach(function (guide) { return (guide.seen = true); });
        this.state.forceShow = false;
        this.updateCurrentGuide();
    },
    onNextStep: function () {
        this.state.currentStep += 1;
        this.trigger(this.state);
    },
    onToStep: function (step) {
        this.state.currentStep = step;
        this.trigger(this.state);
    },
    onRegisterAnchor: function (target) {
        this.state.anchors.add(target);
        this.updateCurrentGuide();
    },
    onUnregisterAnchor: function (target) {
        this.state.anchors.delete(target);
        this.updateCurrentGuide();
    },
    recordCue: function (guide) {
        var user = configStore_1.default.get('user');
        if (!user) {
            return;
        }
        var data = {
            guide: guide,
            eventKey: 'assistant.guide_cued',
            eventName: 'Assistant Guide Cued',
            organization_id: this.state.orgId,
            user_id: parseInt(user.id, 10),
        };
        analytics_1.trackAnalyticsEvent(data);
    },
    updatePrevGuide: function (nextGuide) {
        var prevGuide = this.state.prevGuide;
        if (!nextGuide) {
            return;
        }
        if (!prevGuide || prevGuide.guide !== nextGuide.guide) {
            this.recordCue(nextGuide.guide);
            this.state.prevGuide = nextGuide;
        }
    },
    /**
     * Logic to determine if a guide is shown:
     *
     *  - If any required target is missing, don't show the guide
     *  - If the URL ends with #assistant, show the guide
     *  - If the user has already seen the guide, don't show the guide
     *  - Otherwise show the guide
     */
    updateCurrentGuide: function () {
        var _a = this.state, anchors = _a.anchors, guides = _a.guides, forceShow = _a.forceShow;
        var guideOptions = guides
            .sort(guidePrioritySort)
            .filter(function (guide) { return guide.requiredTargets.every(function (target) { return anchors.has(target); }); });
        var user = configStore_1.default.get('user');
        var assistantThreshold = new Date(2019, 6, 1);
        var userDateJoined = new Date(user === null || user === void 0 ? void 0 : user.dateJoined);
        if (!forceShow) {
            guideOptions = guideOptions.filter(function (_a) {
                var seen = _a.seen, dateThreshold = _a.dateThreshold;
                if (seen) {
                    return false;
                }
                else if (user === null || user === void 0 ? void 0 : user.isSuperuser) {
                    return true;
                }
                else if (dateThreshold) {
                    // Show the guide to users who've joined before the date threshold
                    return userDateJoined < dateThreshold;
                }
                else {
                    return userDateJoined > assistantThreshold;
                }
            });
        }
        var nextGuide = guideOptions.length > 0
            ? tslib_1.__assign(tslib_1.__assign({}, guideOptions[0]), { steps: guideOptions[0].steps.filter(function (step) { return step.target && anchors.has(step.target); }) }) : null;
        this.updatePrevGuide(nextGuide);
        this.state.currentStep =
            this.state.currentGuide &&
                nextGuide &&
                this.state.currentGuide.guide === nextGuide.guide
                ? this.state.currentStep
                : 0;
        this.state.currentGuide = nextGuide;
        this.trigger(this.state);
    },
};
var GuideStore = reflux_1.default.createStore(guideStoreConfig);
exports.default = GuideStore;
//# sourceMappingURL=guideStore.jsx.map