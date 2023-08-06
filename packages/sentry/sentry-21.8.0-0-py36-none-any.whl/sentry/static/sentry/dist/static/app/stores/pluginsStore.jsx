Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var pluginActions_1 = tslib_1.__importDefault(require("app/actions/pluginActions"));
var defaultState = {
    loading: true,
    plugins: [],
    error: null,
    pageLinks: null,
};
var PluginStoreConfig = {
    plugins: null,
    state: tslib_1.__assign({}, defaultState),
    updating: new Map(),
    reset: function () {
        // reset our state
        this.plugins = null;
        this.state = tslib_1.__assign({}, defaultState);
        this.updating = new Map();
        return this.state;
    },
    getInitialState: function () {
        return this.getState();
    },
    getState: function () {
        var _a = this.state, _plugins = _a.plugins, state = tslib_1.__rest(_a, ["plugins"]);
        return tslib_1.__assign(tslib_1.__assign({}, state), { plugins: this.plugins ? Array.from(this.plugins.values()) : [] });
    },
    init: function () {
        this.reset();
        this.listenTo(pluginActions_1.default.fetchAll, this.onFetchAll);
        this.listenTo(pluginActions_1.default.fetchAllSuccess, this.onFetchAllSuccess);
        this.listenTo(pluginActions_1.default.fetchAllError, this.onFetchAllError);
        this.listenTo(pluginActions_1.default.update, this.onUpdate);
        this.listenTo(pluginActions_1.default.updateSuccess, this.onUpdateSuccess);
        this.listenTo(pluginActions_1.default.updateError, this.onUpdateError);
    },
    triggerState: function () {
        this.trigger(this.getState());
    },
    onFetchAll: function (_a) {
        var _b = _a === void 0 ? {} : _a, resetLoading = _b.resetLoading;
        if (resetLoading) {
            this.state.loading = true;
            this.state.error = null;
            this.plugins = null;
        }
        this.triggerState();
    },
    onFetchAllSuccess: function (data, _a) {
        var pageLinks = _a.pageLinks;
        this.plugins = new Map(data.map(function (plugin) { return [plugin.id, plugin]; }));
        this.state.pageLinks = pageLinks || null;
        this.state.loading = false;
        this.triggerState();
    },
    onFetchAllError: function (err) {
        this.plugins = null;
        this.state.loading = false;
        this.state.error = err;
        this.triggerState();
    },
    onUpdate: function (id, updateObj) {
        if (!this.plugins) {
            return;
        }
        var plugin = this.plugins.get(id);
        if (!plugin) {
            return;
        }
        var newPlugin = tslib_1.__assign(tslib_1.__assign({}, plugin), updateObj);
        this.plugins.set(id, newPlugin);
        this.updating.set(id, plugin);
        this.triggerState();
    },
    onUpdateSuccess: function (id, _updateObj) {
        this.updating.delete(id);
    },
    onUpdateError: function (id, _updateObj, err) {
        var origPlugin = this.updating.get(id);
        if (!origPlugin || !this.plugins) {
            return;
        }
        this.plugins.set(id, origPlugin);
        this.updating.delete(id);
        this.state.error = err;
        this.triggerState();
    },
};
var PluginStore = reflux_1.default.createStore(PluginStoreConfig);
exports.default = PluginStore;
//# sourceMappingURL=pluginsStore.jsx.map