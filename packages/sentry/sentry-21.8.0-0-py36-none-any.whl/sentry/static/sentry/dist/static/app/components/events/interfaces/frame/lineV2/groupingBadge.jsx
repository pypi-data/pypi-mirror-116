Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var repoLabel_1 = tslib_1.__importDefault(require("app/components/repoLabel"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var types_1 = require("app/types");
function GroupingBadge(_a) {
    var badge = _a.badge, theme = _a.theme;
    switch (badge) {
        case types_1.FrameBadge.PREFIX:
            return (<tooltip_1.default title={locale_1.t('This frame is used for grouping as prefix frame')} containerDisplayMode="inline-flex">
          <StyledRepoLabel background={theme.green300}>{'prefix'}</StyledRepoLabel>
        </tooltip_1.default>);
        case types_1.FrameBadge.SENTINEL:
            return (<tooltip_1.default title={locale_1.t('This frame is used for grouping as sentinel frame')} containerDisplayMode="inline-flex">
          <StyledRepoLabel background={theme.pink300}>{'sentinel'}</StyledRepoLabel>
        </tooltip_1.default>);
        case types_1.FrameBadge.GROUPING:
            return (<tooltip_1.default title={locale_1.t('This frame is used for grouping')} containerDisplayMode="inline-flex">
          <StyledRepoLabel>{'grouping'}</StyledRepoLabel>
        </tooltip_1.default>);
        default: {
            Sentry.withScope(function (scope) {
                scope.setExtra('badge', badge);
                Sentry.captureException(new Error('Unknown grouping badge'));
            });
            return null;
        }
    }
}
exports.default = react_1.withTheme(GroupingBadge);
var StyledRepoLabel = styled_1.default(repoLabel_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return p.background && "background: " + p.background + ";"; });
var templateObject_1;
//# sourceMappingURL=groupingBadge.jsx.map