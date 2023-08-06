Object.defineProperty(exports, "__esModule", { value: true });
exports.Slider = void 0;
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
function RangeSlider(_a) {
    var _b;
    var value = _a.value, allowedValues = _a.allowedValues, showCustomInput = _a.showCustomInput, name = _a.name, disabled = _a.disabled, placeholder = _a.placeholder, formatLabel = _a.formatLabel, className = _a.className, onBlur = _a.onBlur, onChange = _a.onChange, forwardRef = _a.forwardRef, _c = _a.showLabel, showLabel = _c === void 0 ? true : _c, props = tslib_1.__rest(_a, ["value", "allowedValues", "showCustomInput", "name", "disabled", "placeholder", "formatLabel", "className", "onBlur", "onChange", "forwardRef", "showLabel"]);
    var _d = tslib_1.__read(react_1.useState(allowedValues ? allowedValues.indexOf(Number(value || 0)) : value), 2), sliderValue = _d[0], setSliderValue = _d[1];
    react_1.useEffect(function () {
        updateSliderValue();
    }, [value]);
    function updateSliderValue() {
        var _a;
        if (!utils_1.defined(value)) {
            return;
        }
        var newSliderValueIndex = (_a = allowedValues === null || allowedValues === void 0 ? void 0 : allowedValues.indexOf(Number(value || 0))) !== null && _a !== void 0 ? _a : -1;
        // If `allowedValues` is defined, then `sliderValue` represents index to `allowedValues`
        if (newSliderValueIndex > -1) {
            setSliderValue(newSliderValueIndex);
            return;
        }
        setSliderValue(value);
    }
    function getActualValue(newSliderValue) {
        if (!allowedValues) {
            return newSliderValue;
        }
        // If `allowedValues` is defined, then `sliderValue` represents index to `allowedValues`
        return allowedValues[newSliderValue];
    }
    function handleInput(e) {
        var newSliderValue = parseInt(e.target.value, 10);
        setSliderValue(newSliderValue);
        onChange === null || onChange === void 0 ? void 0 : onChange(getActualValue(newSliderValue), e);
    }
    function handleCustomInputChange(e) {
        setSliderValue(parseInt(e.target.value, 10) || 0);
    }
    function handleBlur(e) {
        if (typeof onBlur !== 'function') {
            return;
        }
        onBlur(e);
    }
    function getSliderData() {
        if (!allowedValues) {
            var min_1 = props.min, max_1 = props.max, step_1 = props.step;
            return {
                min: min_1,
                max: max_1,
                step: step_1,
                actualValue: sliderValue,
                displayValue: sliderValue,
            };
        }
        var actualValue = allowedValues[sliderValue];
        return {
            step: 1,
            min: 0,
            max: allowedValues.length - 1,
            actualValue: actualValue,
            displayValue: utils_1.defined(actualValue) ? actualValue : locale_1.t('Invalid value'),
        };
    }
    var _e = getSliderData(), min = _e.min, max = _e.max, step = _e.step, actualValue = _e.actualValue, displayValue = _e.displayValue;
    return (<div className={className} ref={forwardRef}>
      {!showCustomInput && showLabel && (<Label htmlFor={name}>{(_b = formatLabel === null || formatLabel === void 0 ? void 0 : formatLabel(actualValue)) !== null && _b !== void 0 ? _b : displayValue}</Label>)}
      <SliderAndInputWrapper showCustomInput={showCustomInput}>
        <exports.Slider type="range" name={name} min={min} max={max} step={step} disabled={disabled} onInput={handleInput} onMouseUp={handleBlur} onKeyUp={handleBlur} value={sliderValue} hasLabel={!showCustomInput}/>
        {showCustomInput && (<input_1.default placeholder={placeholder} value={sliderValue} onChange={handleCustomInputChange} onBlur={handleInput}/>)}
      </SliderAndInputWrapper>
    </div>);
}
var RangeSliderContainer = react_1.default.forwardRef(function RangeSliderContainer(props, ref) {
    return <RangeSlider {...props} forwardRef={ref}/>;
});
exports.default = RangeSliderContainer;
exports.Slider = styled_1.default('input')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /* stylelint-disable-next-line property-no-vendor-prefix */\n  -webkit-appearance: none;\n  width: 100%;\n  background: transparent;\n  margin: ", "px 0 ", "px;\n\n  &::-webkit-slider-runnable-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-moz-range-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-ms-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-webkit-slider-thumb {\n    box-shadow: 0 0 0 3px ", ";\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-moz-range-thumb {\n    box-shadow: 0 0 0 3px ", ";\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-thumb {\n    box-shadow: 0 0 0 3px ", ";\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-fill-lower {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &::-ms-fill-upper {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &:focus {\n    outline: none;\n\n    &::-webkit-slider-runnable-track {\n      background: ", ";\n    }\n\n    &::-ms-fill-upper {\n      background: ", ";\n    }\n\n    &::-ms-fill-lower {\n      background: ", ";\n    }\n  }\n\n  &[disabled] {\n    &::-webkit-slider-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-moz-range-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-ms-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-webkit-slider-runnable-track {\n      cursor: default;\n    }\n\n    &::-moz-range-track {\n      cursor: default;\n    }\n\n    &::-ms-track {\n      cursor: default;\n    }\n  }\n"], ["\n  /* stylelint-disable-next-line property-no-vendor-prefix */\n  -webkit-appearance: none;\n  width: 100%;\n  background: transparent;\n  margin: ", "px 0 ", "px;\n\n  &::-webkit-slider-runnable-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-moz-range-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-ms-track {\n    width: 100%;\n    height: 3px;\n    cursor: pointer;\n    background: ", ";\n    border-radius: 3px;\n    border: 0;\n  }\n\n  &::-webkit-slider-thumb {\n    box-shadow: 0 0 0 3px ", ";\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-moz-range-thumb {\n    box-shadow: 0 0 0 3px ", ";\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-thumb {\n    box-shadow: 0 0 0 3px ", ";\n    height: 17px;\n    width: 17px;\n    border-radius: 50%;\n    background: ", ";\n    cursor: pointer;\n    /* stylelint-disable-next-line property-no-vendor-prefix */\n    -webkit-appearance: none;\n    margin-top: -7px;\n    border: 0;\n  }\n\n  &::-ms-fill-lower {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &::-ms-fill-upper {\n    background: ", ";\n    border: 0;\n    border-radius: 50%;\n  }\n\n  &:focus {\n    outline: none;\n\n    &::-webkit-slider-runnable-track {\n      background: ", ";\n    }\n\n    &::-ms-fill-upper {\n      background: ", ";\n    }\n\n    &::-ms-fill-lower {\n      background: ", ";\n    }\n  }\n\n  &[disabled] {\n    &::-webkit-slider-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-moz-range-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-ms-thumb {\n      background: ", ";\n      cursor: default;\n    }\n\n    &::-webkit-slider-runnable-track {\n      cursor: default;\n    }\n\n    &::-moz-range-track {\n      cursor: default;\n    }\n\n    &::-ms-track {\n      cursor: default;\n    }\n  }\n"])), function (p) { return p.theme.grid; }, function (p) { return p.theme.grid * (p.hasLabel ? 2 : 1); }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.background; }, function (p) { return p.theme.active; }, function (p) { return p.theme.background; }, function (p) { return p.theme.active; }, function (p) { return p.theme.background; }, function (p) { return p.theme.active; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; }, function (p) { return p.theme.border; });
var Label = styled_1.default('label')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: 14px;\n  margin-bottom: ", "px;\n  color: ", ";\n"], ["\n  font-size: 14px;\n  margin-bottom: ", "px;\n  color: ", ";\n"])), function (p) { return p.theme.grid; }, function (p) { return p.theme.subText; });
var SliderAndInputWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-auto-flow: column;\n  grid-template-columns: 4fr ", ";\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-auto-flow: column;\n  grid-template-columns: 4fr ", ";\n  grid-gap: ", ";\n"])), function (p) { return p.showCustomInput && '1fr'; }, space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=rangeSlider.jsx.map