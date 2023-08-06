Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var builtInRepositories_1 = tslib_1.__importDefault(require("./builtInRepositories"));
var customRepositories_1 = tslib_1.__importDefault(require("./customRepositories"));
function ExternalSources(_a) {
    var api = _a.api, organization = _a.organization, customRepositories = _a.customRepositories, builtinSymbolSources = _a.builtinSymbolSources, builtinSymbolSourceOptions = _a.builtinSymbolSourceOptions, projectSlug = _a.projectSlug, location = _a.location, router = _a.router;
    return (<react_1.Fragment>
      <builtInRepositories_1.default api={api} organization={organization} builtinSymbolSources={builtinSymbolSources} builtinSymbolSourceOptions={builtinSymbolSourceOptions} projectSlug={projectSlug}/>
      <customRepositories_1.default api={api} location={location} router={router} organization={organization} customRepositories={customRepositories} projectSlug={projectSlug}/>
    </react_1.Fragment>);
}
exports.default = ExternalSources;
//# sourceMappingURL=index.jsx.map