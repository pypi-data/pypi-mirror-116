Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var groupingBadge_1 = tslib_1.__importDefault(require("./groupingBadge"));
function GroupingBadges(_a) {
    var isPrefix = _a.isPrefix, isSentinel = _a.isSentinel, isUsedForGrouping = _a.isUsedForGrouping;
    var badges = [];
    if (isUsedForGrouping && isSentinel) {
        badges.push(<groupingBadge_1.default key={types_1.FrameBadge.SENTINEL} badge={types_1.FrameBadge.SENTINEL}/>);
    }
    if (isUsedForGrouping && isPrefix) {
        badges.push(<groupingBadge_1.default key={types_1.FrameBadge.PREFIX} badge={types_1.FrameBadge.PREFIX}/>);
    }
    if (isUsedForGrouping) {
        badges.push(<groupingBadge_1.default key={types_1.FrameBadge.GROUPING} badge={types_1.FrameBadge.GROUPING}/>);
    }
    return <Wrapper hasGroupingBadges={!!badges.length}>{badges}</Wrapper>;
}
exports.default = GroupingBadges;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: flex-start;\n  justify-content: flex-start;\n  order: 2;\n  grid-column-start: 1;\n  grid-column-end: -1;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    justify-content: flex-end;\n    order: 0;\n    grid-column-start: auto;\n    grid-column-end: auto;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: flex-start;\n  justify-content: flex-start;\n  order: 2;\n  grid-column-start: 1;\n  grid-column-end: -1;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    justify-content: flex-end;\n    order: 0;\n    grid-column-start: auto;\n    grid-column-end: auto;\n  }\n"])), space_1.default(0.5), function (p) { return (p.hasGroupingBadges ? space_1.default(1) : 0); }, function (props) { return props.theme.breakpoints[0]; });
var templateObject_1;
//# sourceMappingURL=groupingBadges.jsx.map