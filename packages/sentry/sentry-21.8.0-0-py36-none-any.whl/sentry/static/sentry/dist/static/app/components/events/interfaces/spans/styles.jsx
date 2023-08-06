Object.defineProperty(exports, "__esModule", { value: true });
exports.MeasurementMarker = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var constants_1 = require("app/components/performance/waterfall/constants");
exports.MeasurementMarker = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  user-select: none;\n  width: 1px;\n  background: repeating-linear-gradient(\n      to bottom,\n      transparent 0 4px,\n      ", " 4px 8px\n    )\n    80%/2px 100% no-repeat;\n  z-index: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  top: 0;\n  height: ", "px;\n  user-select: none;\n  width: 1px;\n  background: repeating-linear-gradient(\n      to bottom,\n      transparent 0 4px,\n      ", " 4px 8px\n    )\n    80%/2px 100% no-repeat;\n  z-index: ", ";\n  color: ", ";\n"])), constants_1.ROW_HEIGHT, function (p) { return (p.failedThreshold ? p.theme.red300 : 'black'); }, function (p) { return p.theme.zIndex.traceView.dividerLine; }, function (p) { return p.theme.textColor; });
var templateObject_1;
//# sourceMappingURL=styles.jsx.map