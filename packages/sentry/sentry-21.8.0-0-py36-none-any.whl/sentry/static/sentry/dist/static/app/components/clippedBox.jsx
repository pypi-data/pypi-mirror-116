Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var color_1 = tslib_1.__importDefault(require("color"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ClippedBox = /** @class */ (function (_super) {
    tslib_1.__extends(ClippedBox, _super);
    function ClippedBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isClipped: !!_this.props.defaultClipped,
            isRevealed: false,
            renderedHeight: _this.props.renderedHeight,
        };
        _this.reveal = function () {
            var onReveal = _this.props.onReveal;
            _this.setState({
                isClipped: false,
                isRevealed: true,
            });
            if (onReveal) {
                onReveal();
            }
        };
        _this.handleClickReveal = function (event) {
            event.stopPropagation();
            _this.reveal();
        };
        return _this;
    }
    ClippedBox.prototype.componentDidMount = function () {
        // eslint-disable-next-line react/no-find-dom-node
        var renderedHeight = react_dom_1.default.findDOMNode(this).offsetHeight;
        this.calcHeight(renderedHeight);
    };
    ClippedBox.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.renderedHeight !== this.props.renderedHeight) {
            this.setRenderedHeight();
        }
        if (prevState.renderedHeight !== this.state.renderedHeight) {
            this.calcHeight(this.state.renderedHeight);
        }
        if (this.state.isRevealed || !this.state.isClipped) {
            return;
        }
        if (!this.props.renderedHeight) {
            // eslint-disable-next-line react/no-find-dom-node
            var renderedHeight = react_dom_1.default.findDOMNode(this).offsetHeight;
            if (renderedHeight < this.props.clipHeight) {
                this.reveal();
            }
        }
    };
    ClippedBox.prototype.setRenderedHeight = function () {
        this.setState({
            renderedHeight: this.props.renderedHeight,
        });
    };
    ClippedBox.prototype.calcHeight = function (renderedHeight) {
        if (!renderedHeight) {
            return;
        }
        if (!this.state.isClipped && renderedHeight > this.props.clipHeight) {
            /* eslint react/no-did-mount-set-state:0 */
            // okay if this causes re-render; cannot determine until
            // rendered first anyways
            this.setState({
                isClipped: true,
            });
        }
    };
    ClippedBox.prototype.render = function () {
        var _a = this.state, isClipped = _a.isClipped, isRevealed = _a.isRevealed;
        var _b = this.props, title = _b.title, children = _b.children, clipHeight = _b.clipHeight, btnText = _b.btnText, className = _b.className;
        return (<ClipWrapper clipHeight={clipHeight} isClipped={isClipped} isRevealed={isRevealed} className={className}>
        {title && <Title>{title}</Title>}
        {children}
        {isClipped && (<ClipFade>
            <button_1.default onClick={this.reveal} priority="primary" size="xsmall">
              {btnText}
            </button_1.default>
          </ClipFade>)}
      </ClipWrapper>);
    };
    ClippedBox.defaultProps = {
        defaultClipped: false,
        clipHeight: 200,
        btnText: locale_1.t('Show More'),
    };
    return ClippedBox;
}(React.PureComponent));
exports.default = ClippedBox;
var ClipWrapper = styled_1.default('div', {
    shouldForwardProp: function (prop) {
        return prop !== 'clipHeight' && prop !== 'isClipped' && prop !== 'isRevealed';
    },
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  margin-left: -", ";\n  margin-right: -", ";\n  padding: ", " ", " 0;\n  border-top: 1px solid ", ";\n  transition: all 5s ease-in-out;\n\n  /* For \"Show More\" animation */\n  ", ";\n\n  ", ";\n\n  :first-of-type {\n    margin-top: -", ";\n    border: 0;\n  }\n"], ["\n  position: relative;\n  margin-left: -", ";\n  margin-right: -", ";\n  padding: ", " ", " 0;\n  border-top: 1px solid ", ";\n  transition: all 5s ease-in-out;\n\n  /* For \"Show More\" animation */\n  ", ";\n\n  ", ";\n\n  :first-of-type {\n    margin-top: -", ";\n    border: 0;\n  }\n"])), space_1.default(3), space_1.default(3), space_1.default(2), space_1.default(3), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.isRevealed && "max-height: 50000px"; }, function (p) {
    return p.isClipped &&
        "\n    max-height: " + p.clipHeight + "px;\n    overflow: hidden;\n  ";
}, space_1.default(2));
var Title = styled_1.default('h5')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
var ClipFade = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  padding: 40px 0 0;\n  background-image: linear-gradient(\n    180deg,\n    ", ",\n    ", "\n  );\n  text-align: center;\n  border-bottom: ", " solid ", ";\n\n  /* Let pointer-events pass through ClipFade to visible elements underneath it */\n  pointer-events: none;\n\n  /* Ensure pointer-events trigger event listeners on \"Expand\" button */\n  > * {\n    pointer-events: auto;\n  }\n"], ["\n  position: absolute;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  padding: 40px 0 0;\n  background-image: linear-gradient(\n    180deg,\n    ", ",\n    ", "\n  );\n  text-align: center;\n  border-bottom: ", " solid ", ";\n\n  /* Let pointer-events pass through ClipFade to visible elements underneath it */\n  pointer-events: none;\n\n  /* Ensure pointer-events trigger event listeners on \"Expand\" button */\n  > * {\n    pointer-events: auto;\n  }\n"])), function (p) { return color_1.default(p.theme.background).alpha(0.15).string(); }, function (p) { return p.theme.background; }, space_1.default(1.5), function (p) { return p.theme.background; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=clippedBox.jsx.map