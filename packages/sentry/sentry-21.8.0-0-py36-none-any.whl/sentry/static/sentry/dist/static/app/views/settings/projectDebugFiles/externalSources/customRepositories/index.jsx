Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var dropdownButton_1 = tslib_1.__importDefault(require("app/components/dropdownButton"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var menuItem_1 = tslib_1.__importDefault(require("app/components/menuItem"));
var panels_1 = require("app/components/panels");
var appStoreConnectContext_1 = tslib_1.__importDefault(require("app/components/projects/appStoreConnectContext"));
var locale_1 = require("app/locale");
var debugFiles_1 = require("app/types/debugFiles");
var utils_1 = require("app/utils");
var repository_1 = tslib_1.__importDefault(require("./repository"));
var utils_2 = require("./utils");
function CustomRepositories(_a) {
    var _b;
    var api = _a.api, organization = _a.organization, repositories = _a.customRepositories, projectSlug = _a.projectSlug, router = _a.router, location = _a.location;
    var appStoreConnectContext = react_1.useContext(appStoreConnectContext_1.default);
    react_1.useEffect(function () {
        openDebugFileSourceDialog();
    }, [location.query, appStoreConnectContext]);
    var hasAppConnectStoreFeatureFlag = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('app-store-connect'));
    if (hasAppConnectStoreFeatureFlag &&
        !appStoreConnectContext &&
        !utils_2.dropDownItems.find(function (dropDownItem) { return dropDownItem.value === debugFiles_1.CustomRepoType.APP_STORE_CONNECT; }) &&
        !repositories.find(function (repository) { return repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT; })) {
        utils_2.dropDownItems.push({
            value: debugFiles_1.CustomRepoType.APP_STORE_CONNECT,
            label: utils_2.customRepoTypeLabel[debugFiles_1.CustomRepoType.APP_STORE_CONNECT],
            searchKey: locale_1.t('apple store connect itunes ios'),
        });
    }
    function openDebugFileSourceDialog() {
        var customRepository = location.query.customRepository;
        if (!customRepository) {
            return;
        }
        var itemIndex = repositories.findIndex(function (v) { return v.id === customRepository; });
        var item = repositories[itemIndex];
        if (!item) {
            return;
        }
        modal_1.openDebugFileSourceModal({
            sourceConfig: item,
            sourceType: item.type,
            appStoreConnectContext: appStoreConnectContext,
            onSave: function (updatedItem) {
                return persistData({ updatedItem: updatedItem, index: itemIndex });
            },
            onClose: handleCloseModal,
        });
    }
    function persistData(_a) {
        var updatedItems = _a.updatedItems, updatedItem = _a.updatedItem, index = _a.index, refresh = _a.refresh;
        var items = updatedItems !== null && updatedItems !== void 0 ? updatedItems : [];
        if (updatedItem && utils_1.defined(index)) {
            items = tslib_1.__spreadArray([], tslib_1.__read(repositories));
            items.splice(index, 1, updatedItem);
        }
        var _b = utils_2.getRequestMessages(items.length, repositories.length), successMessage = _b.successMessage, errorMessage = _b.errorMessage;
        var symbolSources = JSON.stringify(items.map(utils_2.expandKeys));
        var promise = api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/", {
            method: 'PUT',
            data: { symbolSources: symbolSources },
        });
        promise.catch(function () {
            indicator_1.addErrorMessage(errorMessage);
        });
        promise.then(function (result) {
            projectActions_1.default.updateSuccess(result);
            indicator_1.addSuccessMessage(successMessage);
            if (refresh) {
                window.location.reload();
            }
        });
        return promise;
    }
    function handleCloseModal() {
        router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { customRepository: undefined, revalidateItunesSession: undefined }) }));
    }
    function handleAddRepository(repoType) {
        modal_1.openDebugFileSourceModal({
            sourceType: repoType,
            onSave: function (updatedData) {
                return persistData({ updatedItems: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(repositories)), [updatedData]) });
            },
        });
    }
    function handleDeleteRepository(repoId) {
        var newRepositories = tslib_1.__spreadArray([], tslib_1.__read(repositories));
        var index = newRepositories.findIndex(function (item) { return item.id === repoId; });
        newRepositories.splice(index, 1);
        persistData({
            updatedItems: newRepositories,
            refresh: repositories[index].type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT,
        });
    }
    function handleEditRepository(repoId, revalidateItunesSession) {
        router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { customRepository: repoId, revalidateItunesSession: revalidateItunesSession }) }));
    }
    return (<panels_1.Panel>
      <panels_1.PanelHeader hasButtons>
        {locale_1.t('Custom Repositories')}
        <dropdownAutoComplete_1.default alignMenu="right" items={utils_2.dropDownItems.map(function (dropDownItem) { return (tslib_1.__assign(tslib_1.__assign({}, dropDownItem), { label: (<StyledMenuItem onClick={function (event) {
                    event.preventDefault();
                    handleAddRepository(dropDownItem.value);
                }}>
                {dropDownItem.label}
              </StyledMenuItem>) })); })}>
          {function (_a) {
            var isOpen = _a.isOpen;
            return (<dropdownButton_1.default isOpen={isOpen} size="small">
              {locale_1.t('Add Repository')}
            </dropdownButton_1.default>);
        }}
        </dropdownAutoComplete_1.default>
      </panels_1.PanelHeader>
      <panels_1.PanelBody>
        {!repositories.length ? (<emptyStateWarning_1.default>
            <p>{locale_1.t('No custom repositories configured')}</p>
          </emptyStateWarning_1.default>) : (repositories.map(function (repository, index) {
            var repositoryCopy = tslib_1.__assign({}, repository);
            if (repositoryCopy.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT &&
                repositoryCopy.id === (appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.id)) {
                repositoryCopy.details = appStoreConnectContext;
            }
            return (<repository_1.default key={index} repository={repositoryCopy} onDelete={handleDeleteRepository} onEdit={handleEditRepository}/>);
        }))}
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = CustomRepositories;
var StyledMenuItem = styled_1.default(menuItem_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 400;\n  text-transform: none;\n  span {\n    padding: 0;\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 400;\n  text-transform: none;\n  span {\n    padding: 0;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map