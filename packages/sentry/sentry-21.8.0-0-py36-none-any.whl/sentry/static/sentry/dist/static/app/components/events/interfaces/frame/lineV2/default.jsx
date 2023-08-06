Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var iconRefresh_1 = require("app/icons/iconRefresh");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var defaultTitle_1 = tslib_1.__importDefault(require("../defaultTitle"));
var expander_1 = tslib_1.__importDefault(require("./expander"));
var groupingBadges_1 = tslib_1.__importDefault(require("./groupingBadges"));
var wrapper_1 = tslib_1.__importDefault(require("./wrapper"));
function Default(_a) {
    var frame = _a.frame, isHoverPreviewed = _a.isHoverPreviewed, isExpanded = _a.isExpanded, platform = _a.platform, timesRepeated = _a.timesRepeated, isPrefix = _a.isPrefix, isSentinel = _a.isSentinel, isUsedForGrouping = _a.isUsedForGrouping, haveFramesAtLeastOneGroupingBadge = _a.haveFramesAtLeastOneGroupingBadge, haveFramesAtLeastOneExpandedFrame = _a.haveFramesAtLeastOneExpandedFrame, props = tslib_1.__rest(_a, ["frame", "isHoverPreviewed", "isExpanded", "platform", "timesRepeated", "isPrefix", "isSentinel", "isUsedForGrouping", "haveFramesAtLeastOneGroupingBadge", "haveFramesAtLeastOneExpandedFrame"]);
    function renderRepeats() {
        if (utils_1.defined(timesRepeated) && timesRepeated > 0) {
            return (<RepeatedFrames title={locale_1.tn('Frame repeated %s time', 'Frame repeated %s times', timesRepeated)}>
          <RepeatedContent>
            <StyledIconRefresh />
            <span>{timesRepeated}</span>
          </RepeatedContent>
        </RepeatedFrames>);
        }
        return null;
    }
    return (<wrapper_1.default className="title" haveFramesAtLeastOneGroupingBadge={haveFramesAtLeastOneGroupingBadge} haveFramesAtLeastOneExpandedFrame={haveFramesAtLeastOneExpandedFrame}>
      <VertCenterWrapper>
        <defaultTitle_1.default frame={frame} platform={platform} isHoverPreviewed={isHoverPreviewed}/>
        {renderRepeats()}
      </VertCenterWrapper>
      {haveFramesAtLeastOneGroupingBadge && (<groupingBadges_1.default isPrefix={isPrefix} isSentinel={isSentinel} isUsedForGrouping={isUsedForGrouping}/>)}
      <expander_1.default isExpanded={isExpanded} isHoverPreviewed={isHoverPreviewed} platform={platform} {...props}/>
    </wrapper_1.default>);
}
exports.default = Default;
var VertCenterWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  @media (min-width: ", ") {\n    align-items: center;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  @media (min-width: ", ") {\n    align-items: center;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var RepeatedContent = styled_1.default(VertCenterWrapper)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  justify-content: center;\n"], ["\n  justify-content: center;\n"])));
var RepeatedFrames = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  border-radius: 50px;\n  padding: 1px 3px;\n  margin-left: ", ";\n  border-width: thin;\n  border-style: solid;\n  border-color: ", ";\n  color: ", ";\n  background-color: ", ";\n  white-space: nowrap;\n"], ["\n  display: inline-block;\n  border-radius: 50px;\n  padding: 1px 3px;\n  margin-left: ", ";\n  border-width: thin;\n  border-style: solid;\n  border-color: ", ";\n  color: ", ";\n  background-color: ", ";\n  white-space: nowrap;\n"])), space_1.default(1), function (p) { return p.theme.orange500; }, function (p) { return p.theme.orange500; }, function (p) { return p.theme.backgroundSecondary; });
var StyledIconRefresh = styled_1.default(iconRefresh_1.IconRefresh)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.25));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=default.jsx.map