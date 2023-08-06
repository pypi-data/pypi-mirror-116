Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var guideAnchor_1 = require("app/components/assistant/guideAnchor");
var smartSearchBar_1 = tslib_1.__importDefault(require("app/components/smartSearchBar"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var supportedTags = {
    'release.version': {
        key: 'release.version',
        name: 'release.version',
    },
    'release.build': {
        key: 'release.build',
        name: 'release.build',
    },
    'release.package': {
        key: 'release.package',
        name: 'release.package',
    },
    'release.stage': {
        key: 'release.stage',
        name: 'release.stage',
        predefined: true,
        values: constants_1.RELEASE_ADOPTION_STAGES,
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
function ProjectFilters(_a) {
    var _this = this;
    var query = _a.query, tagValueLoader = _a.tagValueLoader, onSearch = _a.onSearch;
    var getTagValues = function (tag, currentQuery) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
        var values;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, tagValueLoader(tag.key, currentQuery)];
                case 1:
                    values = _a.sent();
                    return [2 /*return*/, values.map(function (_a) {
                            var value = _a.value;
                            return value;
                        })];
            }
        });
    }); };
    return (<guideAnchor_1.GuideAnchor target="releases_search" position="bottom">
      <smartSearchBar_1.default searchSource="project_filters" query={query} placeholder={locale_1.t('Search by release version')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={onSearch} onGetTagValues={getTagValues}/>
    </guideAnchor_1.GuideAnchor>);
}
exports.default = ProjectFilters;
//# sourceMappingURL=projectFilters.jsx.map