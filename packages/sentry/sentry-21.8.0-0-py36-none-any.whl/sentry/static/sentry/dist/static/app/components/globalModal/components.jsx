Object.defineProperty(exports, "__esModule", { value: true });
exports.ModalFooter = exports.ModalBody = exports.makeCloseButton = exports.makeClosableHeader = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var iconClose_1 = require("app/icons/iconClose");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ModalHeader = styled_1.default('header')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  margin: -", " -", " ", " -", ";\n\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6 {\n    font-size: 20px;\n    font-weight: 600;\n    margin-bottom: 0;\n    line-height: 1.1;\n  }\n"], ["\n  position: relative;\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  margin: -", " -", " ", " -", ";\n\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6 {\n    font-size: 20px;\n    font-weight: 600;\n    margin-bottom: 0;\n    line-height: 1.1;\n  }\n"])), function (p) { return p.theme.border; }, space_1.default(3), space_1.default(4), space_1.default(4), space_1.default(4), space_1.default(3), space_1.default(4));
var CloseButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n  transform: translate(50%, -50%);\n  border-radius: 50%;\n  background: ", ";\n  height: 24px;\n  width: 24px;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n  transform: translate(50%, -50%);\n  border-radius: 50%;\n  background: ", ";\n  height: 24px;\n  width: 24px;\n"])), function (p) { return p.theme.background; });
CloseButton.defaultProps = {
    label: locale_1.t('Close Modal'),
    icon: <iconClose_1.IconClose size="10px"/>,
    size: 'zero',
};
var ModalBody = styled_1.default('section')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 15px;\n\n  p:last-child {\n    margin-bottom: 0;\n  }\n\n  img {\n    max-width: 100%;\n  }\n"], ["\n  font-size: 15px;\n\n  p:last-child {\n    margin-bottom: 0;\n  }\n\n  img {\n    max-width: 100%;\n  }\n"])));
exports.ModalBody = ModalBody;
var ModalFooter = styled_1.default('footer')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  display: flex;\n  justify-content: flex-end;\n  padding: ", " ", ";\n  margin: ", " -", " -", ";\n"], ["\n  border-top: 1px solid ", ";\n  display: flex;\n  justify-content: flex-end;\n  padding: ", " ", ";\n  margin: ", " -", " -", ";\n"])), function (p) { return p.theme.border; }, space_1.default(3), space_1.default(4), space_1.default(3), space_1.default(4), space_1.default(4));
exports.ModalFooter = ModalFooter;
/**
 * Creates a ModalHeader that includes props to enable the close button
 */
var makeClosableHeader = function (closeModal) {
    var ClosableHeader = function (_a) {
        var closeButton = _a.closeButton, children = _a.children, props = tslib_1.__rest(_a, ["closeButton", "children"]);
        return (<ModalHeader {...props}>
        {children}
        {closeButton && <CloseButton onClick={closeModal}/>}
      </ModalHeader>);
    };
    ClosableHeader.displayName = 'Header';
    return ClosableHeader;
};
exports.makeClosableHeader = makeClosableHeader;
/**
 * Creates a CloseButton component that is connected to the provided closeModal trigger
 */
var makeCloseButton = function (closeModal) {
    return function (props) {
        return <CloseButton {...props} onClick={closeModal}/>;
    };
};
exports.makeCloseButton = makeCloseButton;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=components.jsx.map