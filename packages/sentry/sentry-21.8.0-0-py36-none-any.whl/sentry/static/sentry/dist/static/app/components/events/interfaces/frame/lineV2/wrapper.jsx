Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n\n  ", ";\n\n  @media (min-width: ", ") {\n    align-items: center;\n    grid-gap: ", ";\n    grid-template-columns: ", ";\n  }\n"], ["\n  display: grid;\n\n  ", ";\n\n  @media (min-width: ", ") {\n    align-items: center;\n    grid-gap: ", ";\n    grid-template-columns: ", ";\n  }\n"])), function (p) {
    return p.haveFramesAtLeastOneGroupingBadge && p.haveFramesAtLeastOneExpandedFrame
        ? "\n          grid-template-columns: 1fr 16px;\n          grid-gap: " + space_1.default(1) + ";\n        "
        : p.haveFramesAtLeastOneGroupingBadge
            ? "\n          grid-template-columns: 1fr;\n        "
            : p.haveFramesAtLeastOneExpandedFrame
                ? "\n          grid-template-columns: 1fr 16px;\n          grid-gap: " + space_1.default(1) + ";\n        "
                : "\n          grid-template-columns: 1fr;\n        ";
}, function (props) { return props.theme.breakpoints[0]; }, space_1.default(1), function (p) {
    return p.haveFramesAtLeastOneGroupingBadge && p.haveFramesAtLeastOneExpandedFrame
        ? '1.5fr 0.5fr 16px'
        : p.haveFramesAtLeastOneGroupingBadge
            ? '1fr 0.5fr'
            : p.haveFramesAtLeastOneExpandedFrame
                ? '1fr 16px'
                : '1fr';
});
exports.default = Wrapper;
var templateObject_1;
//# sourceMappingURL=wrapper.jsx.map