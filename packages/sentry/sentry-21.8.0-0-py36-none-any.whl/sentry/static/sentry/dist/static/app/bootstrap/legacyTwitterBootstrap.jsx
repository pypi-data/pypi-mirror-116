/**
 * This is a re-implementation of some bootstrap functionality that we still
 * depend on in some html templates.
 */
/**
 * Similar to jQuery's `on`, adds an event listener to the root document which
 * will only fire when the selector matches the element which triggered the
 * event.
 */
var addSelectorEventListener = function (type, selector, listener) {
    return document.addEventListener(type, function (event) {
        var target = event.target;
        if (target === null) {
            return;
        }
        if (!(target instanceof HTMLElement)) {
            return;
        }
        if (!target.matches(selector)) {
            return;
        }
        listener(event);
    });
};
/**
 * Tab toggle handlers.
 *
 * @deprecated
 */
addSelectorEventListener('click', '[data-toggle="tab"]', function (event) {
    var _a, _b, _c, _d, _e;
    event.preventDefault();
    var triggerElement = event.target;
    var targetSelector = triggerElement.getAttribute('href');
    if (targetSelector === null) {
        return;
    }
    var targetPanel = document.querySelector(targetSelector);
    if (targetPanel === null) {
        return;
    }
    var container = targetPanel.parentElement;
    var tabs = triggerElement.closest('ul');
    var targetTab = triggerElement.closest('li');
    var lastActiveTab = tabs === null || tabs === void 0 ? void 0 : tabs.querySelector(':scope > .active');
    // Reset the old active tab
    (_a = lastActiveTab === null || lastActiveTab === void 0 ? void 0 : lastActiveTab.classList) === null || _a === void 0 ? void 0 : _a.remove('active');
    (_b = lastActiveTab === null || lastActiveTab === void 0 ? void 0 : lastActiveTab.querySelector(':scope > a')) === null || _b === void 0 ? void 0 : _b.setAttribute('aria-expanded', 'false');
    (_d = (_c = container.querySelector(':scope > .active')) === null || _c === void 0 ? void 0 : _c.classList) === null || _d === void 0 ? void 0 : _d.remove('active');
    // Activate the target
    targetTab === null || targetTab === void 0 ? void 0 : targetTab.classList.add('active');
    (_e = targetTab === null || targetTab === void 0 ? void 0 : targetTab.querySelector(':scope > a')) === null || _e === void 0 ? void 0 : _e.setAttribute('aria-expanded', 'true');
    targetPanel.classList.add('active');
});
/**
 * Remove alerts when the close button is clicked
 *
 * @deprecated
 */
addSelectorEventListener('click', '[data-dismiss="alert"]', function (event) {
    var _a;
    (_a = event.target.closest('.alert')) === null || _a === void 0 ? void 0 : _a.remove();
});
//# sourceMappingURL=legacyTwitterBootstrap.jsx.map