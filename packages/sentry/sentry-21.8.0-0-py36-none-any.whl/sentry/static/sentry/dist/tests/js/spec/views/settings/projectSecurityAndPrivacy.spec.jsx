Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var enzyme_1 = require("sentry-test/enzyme");
var projectSecurityAndPrivacy_1 = tslib_1.__importDefault(require("app/views/settings/projectSecurityAndPrivacy"));
// @ts-expect-error
var org = TestStubs.Organization();
// @ts-expect-error
var project = TestStubs.ProjectDetails();
// @ts-expect-error
var routerContext = TestStubs.routerContext([
    {
        // @ts-expect-error
        router: TestStubs.router({
            params: {
                projectId: project.slug,
                orgId: org.slug,
            },
        }),
    },
]);
function renderComponent(props) {
    var _a;
    var organization = (_a = props === null || props === void 0 ? void 0 : props.organization) !== null && _a !== void 0 ? _a : org;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: "/projects/" + organization.slug + "/" + project.slug + "/",
        method: 'GET',
        body: project,
    });
    return enzyme_1.mountWithTheme(<projectSecurityAndPrivacy_1.default project={project} {...routerContext} {...props} organization={organization}/>);
}
describe('projectSecurityAndPrivacy', function () {
    it('renders form fields', function () {
        var wrapper = renderComponent({});
        expect(wrapper.find('Switch[name="dataScrubber"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('Switch[name="dataScrubberDefaults"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('Switch[name="scrubIPAddresses"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('TextArea[name="sensitiveFields"]').prop('value')).toBe('creditcard\nssn');
        expect(wrapper.find('TextArea[name="safeFields"]').prop('value')).toBe('business-email\ncompany');
    });
    it('disables field when equivalent org setting is true', function () {
        var newOrganization = tslib_1.__assign({}, org);
        newOrganization.dataScrubber = true;
        newOrganization.scrubIPAddresses = false;
        var wrapper = renderComponent({ organization: newOrganization });
        expect(wrapper.find('Switch[name="scrubIPAddresses"]').prop('isDisabled')).toBe(false);
        expect(wrapper.find('Switch[name="scrubIPAddresses"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('Switch[name="dataScrubber"]').prop('isDisabled')).toBe(true);
        expect(wrapper.find('Switch[name="dataScrubber"]').prop('isActive')).toBe(true);
    });
});
//# sourceMappingURL=projectSecurityAndPrivacy.spec.jsx.map