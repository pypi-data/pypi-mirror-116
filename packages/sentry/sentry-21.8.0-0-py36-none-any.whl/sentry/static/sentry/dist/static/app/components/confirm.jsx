Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var modal_1 = require("app/actionCreators/modal");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
function Confirm(_a) {
    var bypass = _a.bypass, renderMessage = _a.renderMessage, renderConfirmButton = _a.renderConfirmButton, renderCancelButton = _a.renderCancelButton, message = _a.message, header = _a.header, disabled = _a.disabled, children = _a.children, onConfirm = _a.onConfirm, onConfirming = _a.onConfirming, onCancel = _a.onCancel, _b = _a.priority, priority = _b === void 0 ? 'primary' : _b, _c = _a.cancelText, cancelText = _c === void 0 ? locale_1.t('Cancel') : _c, _d = _a.confirmText, confirmText = _d === void 0 ? locale_1.t('Confirm') : _d, _e = _a.stopPropagation, stopPropagation = _e === void 0 ? false : _e, _f = _a.disableConfirmButton, disableConfirmButton = _f === void 0 ? false : _f;
    var triggerModal = function (e) {
        if (stopPropagation) {
            e === null || e === void 0 ? void 0 : e.stopPropagation();
        }
        if (disabled) {
            return;
        }
        if (bypass) {
            onConfirm === null || onConfirm === void 0 ? void 0 : onConfirm();
            return;
        }
        onConfirming === null || onConfirming === void 0 ? void 0 : onConfirming();
        var modalProps = {
            priority: priority,
            renderMessage: renderMessage,
            renderConfirmButton: renderConfirmButton,
            renderCancelButton: renderCancelButton,
            message: message,
            confirmText: confirmText,
            cancelText: cancelText,
            header: header,
            onConfirm: onConfirm,
            onCancel: onCancel,
            disableConfirmButton: disableConfirmButton,
        };
        modal_1.openModal(function (renderProps) { return <ConfirmModal {...renderProps} {...modalProps}/>; });
    };
    if (typeof children === 'function') {
        return children({ open: triggerModal });
    }
    if (!React.isValidElement(children)) {
        return null;
    }
    // TODO(ts): Understand why the return type of `cloneElement` is strange
    return React.cloneElement(children, { disabled: disabled, onClick: triggerModal });
}
var ConfirmModal = /** @class */ (function (_super) {
    tslib_1.__extends(ConfirmModal, _super);
    function ConfirmModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            disableConfirmButton: !!_this.props.disableConfirmButton,
            confirmCallback: null,
        };
        _this.confirming = false;
        _this.handleClose = function () {
            var _a = _this.props, disableConfirmButton = _a.disableConfirmButton, onCancel = _a.onCancel, closeModal = _a.closeModal;
            onCancel === null || onCancel === void 0 ? void 0 : onCancel();
            _this.setState({ disableConfirmButton: disableConfirmButton !== null && disableConfirmButton !== void 0 ? disableConfirmButton : false });
            // always reset `confirming` when modal visibility changes
            _this.confirming = false;
            closeModal();
        };
        _this.handleConfirm = function () {
            var _a, _b;
            var _c = _this.props, onConfirm = _c.onConfirm, closeModal = _c.closeModal;
            // `confirming` is used to ensure `onConfirm` or the confirm callback is
            // only called once
            if (!_this.confirming) {
                onConfirm === null || onConfirm === void 0 ? void 0 : onConfirm();
                (_b = (_a = _this.state).confirmCallback) === null || _b === void 0 ? void 0 : _b.call(_a);
            }
            _this.setState({ disableConfirmButton: true });
            _this.confirming = true;
            closeModal();
        };
        return _this;
    }
    Object.defineProperty(ConfirmModal.prototype, "confirmMessage", {
        get: function () {
            var _this = this;
            var _a = this.props, message = _a.message, renderMessage = _a.renderMessage;
            if (typeof renderMessage === 'function') {
                return renderMessage({
                    confirm: this.handleConfirm,
                    close: this.handleClose,
                    disableConfirmButton: function (state) {
                        return _this.setState({ disableConfirmButton: state });
                    },
                    setConfirmCallback: function (confirmCallback) {
                        return _this.setState({ confirmCallback: confirmCallback });
                    },
                });
            }
            if (React.isValidElement(message)) {
                return message;
            }
            return (<p>
        <strong>{message}</strong>
      </p>);
        },
        enumerable: false,
        configurable: true
    });
    ConfirmModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, priority = _a.priority, confirmText = _a.confirmText, cancelText = _a.cancelText, header = _a.header, renderConfirmButton = _a.renderConfirmButton, renderCancelButton = _a.renderCancelButton;
        return (<React.Fragment>
        {header && <Header>{header}</Header>}
        <Body>{this.confirmMessage}</Body>
        <Footer>
          <buttonBar_1.default gap={2}>
            {renderCancelButton ? (renderCancelButton({
                closeModal: this.props.closeModal,
                defaultOnClick: this.handleClose,
            })) : (<button_1.default onClick={this.handleClose}>{cancelText}</button_1.default>)}
            {renderConfirmButton ? (renderConfirmButton({
                closeModal: this.props.closeModal,
                defaultOnClick: this.handleConfirm,
            })) : (<button_1.default data-test-id="confirm-button" disabled={this.state.disableConfirmButton} priority={priority} onClick={this.handleConfirm} autoFocus>
                {confirmText}
              </button_1.default>)}
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    };
    return ConfirmModal;
}(React.Component));
exports.default = Confirm;
//# sourceMappingURL=confirm.jsx.map