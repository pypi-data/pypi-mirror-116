Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/components/performance/waterfall/utils");
var CursorGuideHandler = tslib_1.__importStar(require("./cursorGuideHandler"));
function SpanBarCursorGuide() {
    return (<CursorGuideHandler.Consumer>
      {function (_a) {
            var showCursorGuide = _a.showCursorGuide, traceViewMouseLeft = _a.traceViewMouseLeft;
            if (!showCursorGuide || !traceViewMouseLeft) {
                return null;
            }
            return (<CursorGuide style={{
                    left: utils_1.toPercent(traceViewMouseLeft),
                }}/>);
        }}
    </CursorGuideHandler.Consumer>);
}
var CursorGuide = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n  height: 100%;\n"], ["\n  position: absolute;\n  top: 0;\n  width: 1px;\n  background-color: ", ";\n  transform: translateX(-50%);\n  height: 100%;\n"])), function (p) { return p.theme.red300; });
exports.default = SpanBarCursorGuide;
var templateObject_1;
//# sourceMappingURL=spanBarCursorGuide.jsx.map