Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var highlight_bottom_left_svg_1 = tslib_1.__importDefault(require("sentry-images/pattern/highlight-bottom-left.svg"));
var highlight_top_right_svg_1 = tslib_1.__importDefault(require("sentry-images/pattern/highlight-top-right.svg"));
function HighlightModalContainer(_a) {
    var topWidth = _a.topWidth, bottomWidth = _a.bottomWidth, children = _a.children;
    return (<react_1.Fragment>
      <PositionTopRight src={highlight_top_right_svg_1.default} width={topWidth}/>
      {children}
      <PositionBottomLeft src={highlight_bottom_left_svg_1.default} width={bottomWidth}/>
    </react_1.Fragment>);
}
exports.default = HighlightModalContainer;
var PositionTopRight = styled_1.default('img')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  width: ", ";\n  right: 0;\n  top: 0;\n  pointer-events: none;\n"], ["\n  position: absolute;\n  width: ", ";\n  right: 0;\n  top: 0;\n  pointer-events: none;\n"])), function (p) { return p.width; });
var PositionBottomLeft = styled_1.default('img')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  width: ", ";\n  bottom: 0;\n  left: 0;\n  pointer-events: none;\n"], ["\n  position: absolute;\n  width: ", ";\n  bottom: 0;\n  left: 0;\n  pointer-events: none;\n"])), function (p) { return p.width; });
HighlightModalContainer.defaultProps = {
    topWidth: '400px',
    bottomWidth: '200px',
};
var templateObject_1, templateObject_2;
//# sourceMappingURL=highlightModalContainer.jsx.map