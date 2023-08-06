Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var test_utils_1 = require("react-dom/test-utils");
var createListeners_1 = require("sentry-test/createListeners");
var enzyme_1 = require("sentry-test/enzyme");
var editableText_1 = tslib_1.__importDefault(require("app/components/editableText"));
var currentValue = 'foo';
function renderedComponent(onChange, newValue) {
    if (newValue === void 0) { newValue = 'bar'; }
    var wrapper = enzyme_1.mountWithTheme(<editableText_1.default value={currentValue} onChange={onChange}/>);
    var label = wrapper.find('Label');
    expect(label.text()).toEqual(currentValue);
    var inputWrapper = wrapper.find('InputWrapper');
    expect(inputWrapper.length).toEqual(0);
    var styledIconEdit = wrapper.find('IconEdit');
    expect(styledIconEdit.length).toEqual(1);
    label.simulate('click');
    label = wrapper.find('Label');
    expect(inputWrapper.length).toEqual(0);
    inputWrapper = wrapper.find('InputWrapper');
    expect(inputWrapper.length).toEqual(1);
    var styledInput = wrapper.find('StyledInput');
    expect(styledInput.length).toEqual(1);
    styledInput.simulate('change', { target: { value: newValue } });
    var inputLabel = wrapper.find('InputLabel');
    expect(inputLabel.text()).toEqual(newValue);
    return wrapper;
}
describe('EditableText', function () {
    var newValue = 'bar';
    it('edit value and click outside of the component', function () {
        var fireEvent = createListeners_1.createListeners('document');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange);
        test_utils_1.act(function () {
            // Click outside of the component
            fireEvent.mouseDown(document.body);
        });
        expect(handleChange).toHaveBeenCalled();
        wrapper.update();
        var updatedLabel = wrapper.find('Label');
        expect(updatedLabel.length).toEqual(1);
        expect(updatedLabel.text()).toEqual(newValue);
    });
    it('edit value and press enter', function () {
        var fireEvent = createListeners_1.createListeners('window');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange);
        test_utils_1.act(function () {
            // Press enter
            fireEvent.keyDown('Enter');
        });
        expect(handleChange).toHaveBeenCalled();
        wrapper.update();
        var updatedLabel = wrapper.find('Label');
        expect(updatedLabel.length).toEqual(1);
        expect(updatedLabel.text()).toEqual(newValue);
    });
    it('clear value and show error message', function () {
        var fireEvent = createListeners_1.createListeners('window');
        var handleChange = jest.fn();
        var wrapper = renderedComponent(handleChange, '');
        test_utils_1.act(function () {
            // Press enter
            fireEvent.keyDown('Enter');
        });
        expect(handleChange).toHaveBeenCalledTimes(0);
        wrapper.update();
    });
    it('displays a disabled value', function () {
        var handleChange = jest.fn();
        var wrapper = enzyme_1.mountWithTheme(<editableText_1.default value={currentValue} onChange={handleChange} isDisabled/>);
        var label = wrapper.find('Label');
        expect(label.text()).toEqual(currentValue);
        label.simulate('click');
        var inputWrapper = wrapper.find('InputWrapper');
        expect(inputWrapper.length).toEqual(0);
        label = wrapper.find('Label');
        expect(label.length).toEqual(1);
    });
    describe('revert value and close editor', function () {
        it('prop value changes', function () {
            var handleChange = jest.fn();
            var newPropValue = 'new-prop-value';
            var wrapper = renderedComponent(handleChange, '');
            wrapper.setProps({ value: newPropValue });
            wrapper.update();
            var updatedLabel = wrapper.find('Label');
            expect(updatedLabel.length).toEqual(1);
            expect(updatedLabel.text()).toEqual(newPropValue);
        });
        it('prop isDisabled changes', function () {
            var handleChange = jest.fn();
            var wrapper = renderedComponent(handleChange, '');
            wrapper.setProps({ isDisabled: true });
            wrapper.update();
            var updatedLabel = wrapper.find('Label');
            expect(updatedLabel.length).toEqual(1);
            expect(updatedLabel.text()).toEqual(currentValue);
        });
        it('edit value and press escape', function () {
            var fireEvent = createListeners_1.createListeners('window');
            var handleChange = jest.fn();
            var wrapper = renderedComponent(handleChange);
            test_utils_1.act(function () {
                // Press escape
                fireEvent.keyDown('Escape');
            });
            expect(handleChange).toHaveBeenCalledTimes(0);
            wrapper.update();
            var updatedLabel = wrapper.find('Label');
            expect(updatedLabel.length).toEqual(1);
            expect(updatedLabel.text()).toEqual(currentValue);
        });
    });
});
//# sourceMappingURL=editableText.spec.jsx.map