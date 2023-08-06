Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var messageRow_1 = require("app/components/performance/waterfall/messageRow");
var utils_1 = require("app/components/performance/waterfall/utils");
var locale_1 = require("app/locale");
var scrollbarManager_1 = require("./scrollbarManager");
var spanBar_1 = tslib_1.__importDefault(require("./spanBar"));
var spanGroupBar_1 = tslib_1.__importDefault(require("./spanGroupBar"));
var utils_2 = require("./utils");
var SpanTree = /** @class */ (function (_super) {
    tslib_1.__extends(SpanTree, _super);
    function SpanTree() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.toggleSpanTree = function (spanID) { return function () {
            _this.props.waterfallModel.toggleSpanGroup(spanID);
            // Update horizontal scroll states after this subtree was either hidden or
            // revealed.
            _this.props.updateScrollState();
        }; };
        return _this;
    }
    SpanTree.prototype.shouldComponentUpdate = function (nextProps) {
        if (this.props.dragProps.isDragging !== nextProps.dragProps.isDragging ||
            this.props.dragProps.isWindowSelectionDragging !==
                nextProps.dragProps.isWindowSelectionDragging) {
            return true;
        }
        if (nextProps.dragProps.isDragging ||
            nextProps.dragProps.isWindowSelectionDragging ||
            isEqual_1.default(this.props.spans, nextProps.spans)) {
            return false;
        }
        return true;
    };
    SpanTree.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual_1.default(prevProps.filterSpans, this.props.filterSpans) ||
            !isEqual_1.default(prevProps.spans, this.props.spans)) {
            // Update horizontal scroll states after a search has been performed or if
            // if the spans has changed
            this.props.updateScrollState();
        }
    };
    SpanTree.prototype.generateInfoMessage = function (input) {
        var isCurrentSpanHidden = input.isCurrentSpanHidden, numOfSpansOutOfViewAbove = input.numOfSpansOutOfViewAbove, isCurrentSpanFilteredOut = input.isCurrentSpanFilteredOut, numOfFilteredSpansAbove = input.numOfFilteredSpansAbove;
        var messages = [];
        var showHiddenSpansMessage = !isCurrentSpanHidden && numOfSpansOutOfViewAbove > 0;
        if (showHiddenSpansMessage) {
            messages.push(<span key="spans-out-of-view">
          <strong>{numOfSpansOutOfViewAbove}</strong> {locale_1.t('spans out of view')}
        </span>);
        }
        var showFilteredSpansMessage = !isCurrentSpanFilteredOut && numOfFilteredSpansAbove > 0;
        if (showFilteredSpansMessage) {
            if (!isCurrentSpanHidden) {
                if (numOfFilteredSpansAbove === 1) {
                    messages.push(<span key="spans-filtered">
              {locale_1.tct('[numOfSpans] hidden span', {
                            numOfSpans: <strong>{numOfFilteredSpansAbove}</strong>,
                        })}
            </span>);
                }
                else {
                    messages.push(<span key="spans-filtered">
              {locale_1.tct('[numOfSpans] hidden spans', {
                            numOfSpans: <strong>{numOfFilteredSpansAbove}</strong>,
                        })}
            </span>);
                }
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <messageRow_1.MessageRow>{messages}</messageRow_1.MessageRow>;
    };
    SpanTree.prototype.generateLimitExceededMessage = function () {
        var waterfallModel = this.props.waterfallModel;
        var parsedTrace = waterfallModel.parsedTrace;
        if (hasAllSpans(parsedTrace)) {
            return null;
        }
        return (<messageRow_1.MessageRow>
        {locale_1.t('The next spans are unavailable. You may have exceeded the span limit or need to address missing instrumentation.')}
      </messageRow_1.MessageRow>);
    };
    SpanTree.prototype.render = function () {
        var _this = this;
        var _a = this.props, waterfallModel = _a.waterfallModel, spans = _a.spans, organization = _a.organization, dragProps = _a.dragProps;
        var generateBounds = waterfallModel.generateBounds({
            viewStart: dragProps.viewWindowStart,
            viewEnd: dragProps.viewWindowEnd,
        });
        var _b = spans.reduce(function (acc, payload) {
            var type = payload.type;
            switch (payload.type) {
                case 'filtered_out': {
                    acc.numOfFilteredSpansAbove += 1;
                    return acc;
                }
                case 'out_of_view': {
                    acc.numOfSpansOutOfViewAbove += 1;
                    return acc;
                }
                default: {
                    break;
                }
            }
            var previousSpanNotDisplayed = acc.numOfFilteredSpansAbove > 0 || acc.numOfSpansOutOfViewAbove > 0;
            if (previousSpanNotDisplayed) {
                var infoMessage_1 = _this.generateInfoMessage({
                    isCurrentSpanHidden: false,
                    numOfSpansOutOfViewAbove: acc.numOfSpansOutOfViewAbove,
                    isCurrentSpanFilteredOut: false,
                    numOfFilteredSpansAbove: acc.numOfFilteredSpansAbove,
                });
                acc.spanTree.push(infoMessage_1);
            }
            var spanNumber = acc.spanNumber;
            var span = payload.span, treeDepth = payload.treeDepth, continuingTreeDepths = payload.continuingTreeDepths;
            if (payload.type === 'span_group_chain') {
                acc.spanTree.push(<spanGroupBar_1.default key={spanNumber + "-span-group"} event={waterfallModel.event} span={span} generateBounds={generateBounds} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} spanNumber={spanNumber} spanGrouping={payload.spanGrouping} toggleSpanGroup={payload.toggleSpanGroup}/>);
                acc.spanNumber = spanNumber + 1;
                return acc;
            }
            var key = utils_2.getSpanID(span, "span-" + spanNumber);
            var isLast = payload.isLastSibling;
            var isRoot = type === 'root_span';
            var spanBarColor = utils_1.pickBarColor(utils_2.getSpanOperation(span));
            var numOfSpanChildren = payload.numOfSpanChildren;
            acc.numOfFilteredSpansAbove = 0;
            acc.numOfSpansOutOfViewAbove = 0;
            var toggleSpanGroup = undefined;
            if (payload.type === 'span') {
                toggleSpanGroup = payload.toggleSpanGroup;
            }
            acc.spanTree.push(<spanBar_1.default key={key} organization={organization} event={waterfallModel.event} spanBarColor={spanBarColor} spanBarHatch={type === 'gap'} span={span} showSpanTree={!waterfallModel.hiddenSpanGroups.has(utils_2.getSpanID(span))} numOfSpanChildren={numOfSpanChildren} trace={waterfallModel.parsedTrace} generateBounds={generateBounds} toggleSpanTree={_this.toggleSpanTree(utils_2.getSpanID(span))} treeDepth={treeDepth} continuingTreeDepths={continuingTreeDepths} spanNumber={spanNumber} isLast={isLast} isRoot={isRoot} showEmbeddedChildren={payload.showEmbeddedChildren} toggleEmbeddedChildren={payload.toggleEmbeddedChildren} fetchEmbeddedChildrenState={payload.fetchEmbeddedChildrenState} toggleSpanGroup={toggleSpanGroup}/>);
            acc.spanNumber = spanNumber + 1;
            return acc;
        }, {
            numOfSpansOutOfViewAbove: 0,
            numOfFilteredSpansAbove: 0,
            spanTree: [],
            spanNumber: 1, // 1-based indexing
        }), spanTree = _b.spanTree, numOfSpansOutOfViewAbove = _b.numOfSpansOutOfViewAbove, numOfFilteredSpansAbove = _b.numOfFilteredSpansAbove;
        var infoMessage = this.generateInfoMessage({
            isCurrentSpanHidden: false,
            numOfSpansOutOfViewAbove: numOfSpansOutOfViewAbove,
            isCurrentSpanFilteredOut: false,
            numOfFilteredSpansAbove: numOfFilteredSpansAbove,
        });
        return (<TraceViewContainer ref={this.props.traceViewRef}>
        {spanTree}
        {infoMessage}
        {this.generateLimitExceededMessage()}
      </TraceViewContainer>);
    };
    return SpanTree;
}(React.Component));
var TraceViewContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
/**
 * Checks if a trace contains all of its spans.
 *
 * The heuristic used here favors false negatives over false positives.
 * This is because showing a warning that the trace is not showing all
 * spans when it has them all is more misleading than not showing a
 * warning when it is missing some spans.
 *
 * A simple heuristic to determine when there are unrecorded spans
 *
 * 1. We assume if there are less than 999 spans, then we have all
 *    the spans for a transaction. 999 was chosen because most SDKs
 *    have a default limit of 1000 spans per transaction, but the
 *    python SDK is 999 for historic reasons.
 *
 * 2. We assume that if there are unrecorded spans, they should be
 *    at least 100ms in duration.
 *
 * While not perfect, this simple heuristic is unlikely to report
 * false positives.
 */
function hasAllSpans(trace) {
    var traceEndTimestamp = trace.traceEndTimestamp, spans = trace.spans;
    if (spans.length < 999) {
        return true;
    }
    var lastSpan = spans.reduce(function (latest, span) {
        return latest.timestamp > span.timestamp ? latest : span;
    });
    var missingDuration = traceEndTimestamp - lastSpan.timestamp;
    return missingDuration < 0.1;
}
exports.default = scrollbarManager_1.withScrollbarManager(SpanTree);
var templateObject_1;
//# sourceMappingURL=spanTree.jsx.map