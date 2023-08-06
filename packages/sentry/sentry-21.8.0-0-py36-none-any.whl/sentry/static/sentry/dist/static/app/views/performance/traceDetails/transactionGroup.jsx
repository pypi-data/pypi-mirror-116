Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var scrollbarManager_1 = require("app/components/events/interfaces/spans/scrollbarManager");
var transactionBar_1 = tslib_1.__importDefault(require("./transactionBar"));
var TransactionGroup = /** @class */ (function (_super) {
    tslib_1.__extends(TransactionGroup, _super);
    function TransactionGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isExpanded: true,
        };
        _this.toggleExpandedState = function () {
            _this.setState(function (_a) {
                var isExpanded = _a.isExpanded;
                return ({ isExpanded: !isExpanded });
            });
        };
        return _this;
    }
    TransactionGroup.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.isExpanded !== this.state.isExpanded) {
            this.props.updateScrollState();
        }
    };
    TransactionGroup.prototype.render = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction, traceInfo = _a.traceInfo, continuingDepths = _a.continuingDepths, isOrphan = _a.isOrphan, isLast = _a.isLast, index = _a.index, isVisible = _a.isVisible, hasGuideAnchor = _a.hasGuideAnchor, renderedChildren = _a.renderedChildren, barColor = _a.barColor;
        var isExpanded = this.state.isExpanded;
        return (<React.Fragment>
        <transactionBar_1.default location={location} organization={organization} index={index} transaction={transaction} traceInfo={traceInfo} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} isExpanded={isExpanded} toggleExpandedState={this.toggleExpandedState} isVisible={isVisible} hasGuideAnchor={hasGuideAnchor} barColor={barColor}/>
        {isExpanded && renderedChildren}
      </React.Fragment>);
    };
    return TransactionGroup;
}(React.Component));
exports.default = scrollbarManager_1.withScrollbarManager(TransactionGroup);
//# sourceMappingURL=transactionGroup.jsx.map