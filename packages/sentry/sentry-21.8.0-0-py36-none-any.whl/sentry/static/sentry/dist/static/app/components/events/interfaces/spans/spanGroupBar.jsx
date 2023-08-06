Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var countBy_1 = tslib_1.__importDefault(require("lodash/countBy"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var constants_1 = require("app/components/performance/waterfall/constants");
var row_1 = require("app/components/performance/waterfall/row");
var rowBar_1 = require("app/components/performance/waterfall/rowBar");
var rowDivider_1 = require("app/components/performance/waterfall/rowDivider");
var rowTitle_1 = require("app/components/performance/waterfall/rowTitle");
var treeConnector_1 = require("app/components/performance/waterfall/treeConnector");
var utils_1 = require("app/components/performance/waterfall/utils");
var locale_1 = require("app/locale");
var utils_2 = require("app/utils");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var DividerHandlerManager = tslib_1.__importStar(require("./dividerHandlerManager"));
var ScrollbarManager = tslib_1.__importStar(require("./scrollbarManager"));
var spanBarCursorGuide_1 = tslib_1.__importDefault(require("./spanBarCursorGuide"));
var styles_1 = require("./styles");
var utils_3 = require("./utils");
var MARGIN_LEFT = 0;
var SpanGroupBar = /** @class */ (function (_super) {
    tslib_1.__extends(SpanGroupBar, _super);
    function SpanGroupBar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SpanGroupBar.prototype.getSpanGroupTimestamps = function (spanGroup) {
        return spanGroup.reduce(function (acc, spanGroupItem) {
            var _a = spanGroupItem.span, start_timestamp = _a.start_timestamp, timestamp = _a.timestamp;
            var newStartTimestamp = acc.startTimestamp;
            var newEndTimestamp = acc.endTimestamp;
            if (start_timestamp < newStartTimestamp) {
                newStartTimestamp = start_timestamp;
            }
            if (newEndTimestamp > timestamp) {
                newEndTimestamp = timestamp;
            }
            return {
                startTimestamp: newStartTimestamp,
                endTimestamp: newEndTimestamp,
            };
        }, {
            startTimestamp: spanGroup[0].span.start_timestamp,
            endTimestamp: spanGroup[0].span.timestamp,
        });
    };
    SpanGroupBar.prototype.getSpanGroupBounds = function (spanGroup) {
        var generateBounds = this.props.generateBounds;
        var _a = this.getSpanGroupTimestamps(spanGroup), startTimestamp = _a.startTimestamp, endTimestamp = _a.endTimestamp;
        var bounds = generateBounds({
            startTimestamp: startTimestamp,
            endTimestamp: endTimestamp,
        });
        switch (bounds.type) {
            case 'TRACE_TIMESTAMPS_EQUAL':
            case 'INVALID_VIEW_WINDOW': {
                return {
                    warning: void 0,
                    left: void 0,
                    width: void 0,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_EQUAL': {
                return {
                    warning: void 0,
                    left: bounds.start,
                    width: 0.00001,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            case 'TIMESTAMPS_REVERSED':
            case 'TIMESTAMPS_STABLE': {
                return {
                    warning: void 0,
                    left: bounds.start,
                    width: bounds.end - bounds.start,
                    isSpanVisibleInView: bounds.isSpanVisibleInView,
                };
            }
            default: {
                var _exhaustiveCheck = bounds;
                return _exhaustiveCheck;
            }
        }
    };
    SpanGroupBar.prototype.renderGroupedSpansToggler = function () {
        var _a = this.props, spanGrouping = _a.spanGrouping, treeDepth = _a.treeDepth, toggleSpanGroup = _a.toggleSpanGroup;
        var left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
        return (<treeConnector_1.TreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderSpanTreeConnector()}
        <treeConnector_1.TreeToggle disabled={false} isExpanded={false} errored={false} isSpanGroupToggler onClick={function (event) {
                event.stopPropagation();
                toggleSpanGroup();
            }}>
          <count_1.default value={spanGrouping.length}/>
        </treeConnector_1.TreeToggle>
      </treeConnector_1.TreeToggleContainer>);
    };
    SpanGroupBar.prototype.generateGroupSpansTitle = function (spanGroup) {
        if (spanGroup.length === 0) {
            return '';
        }
        var operationCounts = countBy_1.default(spanGroup, function (enhancedSpan) {
            return utils_3.getSpanOperation(enhancedSpan.span);
        });
        var hasOthers = Object.keys(operationCounts).length > 1;
        var _a = tslib_1.__read(Object.entries(operationCounts).reduce(function (acc, _a) {
            var _b = tslib_1.__read(_a, 2), operationNameKey = _b[0], count = _b[1];
            if (count > acc[1]) {
                return [operationNameKey, count];
            }
            return acc;
        }), 1), mostFrequentOperationName = _a[0];
        return (<strong>{locale_1.t('Autogrouped ') + "\u2014 " + mostFrequentOperationName + (hasOthers ? locale_1.t(' and more') : '')}</strong>);
    };
    SpanGroupBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<rowDivider_1.DividerLine ref={addDividerLineRef()} style={{
                position: 'absolute',
            }} onMouseEnter={function () {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseLeave={function () {
                dividerHandlerChildrenProps.setHover(false);
            }} onMouseOver={function () {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
                // we prevent the propagation of the clicks from this component to prevent
                // the span detail from being opened.
                event.stopPropagation();
            }}/>);
    };
    SpanGroupBar.prototype.renderSpanTreeConnector = function () {
        var _a = this.props, spanTreeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, span = _a.span;
        var connectorBars = continuingTreeDepths.map(function (treeDepth) {
            var depth = utils_3.unwrapTreeDepth(treeDepth);
            if (depth === 0) {
                // do not render a connector bar at depth 0,
                // if we did render a connector bar, this bar would be placed at depth -1
                // which does not exist.
                return null;
            }
            var left = ((spanTreeDepth - depth) * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + 1) * -1;
            return (<treeConnector_1.ConnectorBar style={{ left: left }} key={"span-group-" + depth} orphanBranch={utils_3.isOrphanTreeDepth(treeDepth)}/>);
        });
        connectorBars.push(<treeConnector_1.ConnectorBar style={{
                right: '16px',
                height: constants_1.ROW_HEIGHT / 2 + "px",
                bottom: "-" + constants_1.ROW_HEIGHT / 2 + "px",
                top: 'auto',
            }} key="collapsed-span-group-row-bottom" orphanBranch={false}/>);
        return (<treeConnector_1.TreeConnector isLast hasToggler orphanBranch={utils_3.isOrphanSpan(span)}>
        {connectorBars}
      </treeConnector_1.TreeConnector>);
    };
    SpanGroupBar.prototype.renderMeasurements = function () {
        var _a = this.props, event = _a.event, generateBounds = _a.generateBounds;
        var measurements = utils_3.getMeasurements(event);
        return (<React.Fragment>
        {Array.from(measurements).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], verticalMark = _b[1];
                var bounds = utils_3.getMeasurementBounds(timestamp, generateBounds);
                var shouldDisplay = utils_2.defined(bounds.left) && utils_2.defined(bounds.width);
                if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                    return null;
                }
                return (<styles_1.MeasurementMarker key={String(timestamp)} style={{
                        left: "clamp(0%, " + utils_1.toPercent(bounds.left || 0) + ", calc(100% - 1px))",
                    }} failedThreshold={verticalMark.failedThreshold}/>);
            })}
      </React.Fragment>);
    };
    SpanGroupBar.prototype.render = function () {
        var _this = this;
        return (<ScrollbarManager.Consumer>
        {function (scrollbarManagerChildrenProps) { return (<DividerHandlerManager.Consumer>
            {function (dividerHandlerChildrenProps) {
                    var _a = _this.props, span = _a.span, generateBounds = _a.generateBounds, treeDepth = _a.treeDepth, spanGrouping = _a.spanGrouping, toggleSpanGroup = _a.toggleSpanGroup, spanNumber = _a.spanNumber;
                    var isSpanVisible = generateBounds({
                        startTimestamp: span.start_timestamp,
                        endTimestamp: span.timestamp,
                    }).isSpanVisibleInView;
                    var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
                    var generateContentSpanBarRef = scrollbarManagerChildrenProps.generateContentSpanBarRef;
                    var left = treeDepth * (treeConnector_1.TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
                    var bounds = _this.getSpanGroupBounds(spanGrouping);
                    var durationDisplay = utils_1.getDurationDisplay(bounds);
                    var _b = _this.getSpanGroupTimestamps(spanGrouping), startTimestamp = _b.startTimestamp, endTimestamp = _b.endTimestamp;
                    var duration = Math.abs(endTimestamp - startTimestamp);
                    var durationString = utils_1.getHumanDuration(duration);
                    return (<row_1.Row visible={isSpanVisible} showBorder={false} data-test-id="span-row">
                  <row_1.RowCellContainer>
                    <row_1.RowCell data-type="span-row-cell" style={{
                            width: "calc(" + utils_1.toPercent(dividerPosition) + " - 0.5px)",
                            paddingTop: 0,
                        }} onClick={function () {
                            toggleSpanGroup();
                        }}>
                      <rowTitle_1.RowTitleContainer ref={generateContentSpanBarRef()}>
                        {_this.renderGroupedSpansToggler()}
                        <rowTitle_1.RowTitle style={{
                            left: left + "px",
                            width: '100%',
                        }}>
                          <rowTitle_1.SpanGroupRowTitleContent>
                            {_this.generateGroupSpansTitle(spanGrouping)}
                          </rowTitle_1.SpanGroupRowTitleContent>
                        </rowTitle_1.RowTitle>
                      </rowTitle_1.RowTitleContainer>
                    </row_1.RowCell>
                    <rowDivider_1.DividerContainer>
                      {_this.renderDivider(dividerHandlerChildrenProps)}
                    </rowDivider_1.DividerContainer>
                    <row_1.RowCell data-type="span-row-cell" showStriping={spanNumber % 2 !== 0} style={{
                            width: "calc(" + utils_1.toPercent(1 - dividerPosition) + " - 0.5px)",
                        }} onClick={function () {
                            toggleSpanGroup();
                        }}>
                      <rowBar_1.RowRectangle spanBarHatch={false} style={{
                            backgroundColor: theme_1.default.blue300,
                            left: "min(" + utils_1.toPercent(bounds.left || 0) + ", calc(100% - 1px))",
                            width: utils_1.toPercent(bounds.width || 0),
                        }}>
                        <rowBar_1.DurationPill durationDisplay={durationDisplay} showDetail={false} spanBarHatch={false}>
                          {durationString}
                        </rowBar_1.DurationPill>
                      </rowBar_1.RowRectangle>
                      {_this.renderMeasurements()}
                      <spanBarCursorGuide_1.default />
                    </row_1.RowCell>
                    <rowDivider_1.DividerLineGhostContainer style={{
                            width: "calc(" + utils_1.toPercent(dividerPosition) + " + 0.5px)",
                            display: 'none',
                        }}>
                      <rowDivider_1.DividerLine ref={addGhostDividerLineRef()} style={{
                            right: 0,
                        }} className="hovering" onClick={function (event) {
                            // the ghost divider line should not be interactive.
                            // we prevent the propagation of the clicks from this component to prevent
                            // the span detail from being opened.
                            event.stopPropagation();
                        }}/>
                    </rowDivider_1.DividerLineGhostContainer>
                  </row_1.RowCellContainer>
                </row_1.Row>);
                }}
          </DividerHandlerManager.Consumer>); }}
      </ScrollbarManager.Consumer>);
    };
    return SpanGroupBar;
}(React.Component));
exports.default = SpanGroupBar;
//# sourceMappingURL=spanGroupBar.jsx.map