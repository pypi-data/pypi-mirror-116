Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var stacktracePreview_1 = require("app/components/stacktracePreview");
var iconChevron_1 = require("app/icons/iconChevron");
var locale_1 = require("app/locale");
var utils_1 = require("../utils");
function Expander(_a) {
    var isExpandable = _a.isExpandable, isHoverPreviewed = _a.isHoverPreviewed, isExpanded = _a.isExpanded, platform = _a.platform, onToggleContext = _a.onToggleContext;
    if (!isExpandable) {
        return null;
    }
    return (<StyledButton className="btn-toggle" css={utils_1.isDotnet(platform) && { display: 'block !important' }} // remove important once we get rid of css files
     title={locale_1.t('Toggle Context')} tooltipProps={isHoverPreviewed ? { delay: stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY } : undefined} onClick={onToggleContext}>
      <iconChevron_1.IconChevron direction={isExpanded ? 'up' : 'down'} size="8px"/>
    </StyledButton>);
}
exports.default = Expander;
// the Button's label has the padding of 3px because the button size has to be 16x16 px.
var StyledButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  span:first-child {\n    padding: 3px;\n  }\n"], ["\n  span:first-child {\n    padding: 3px;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=expander.jsx.map