Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var initializeOrg_1 = require("sentry-test/initializeOrg");
var reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
var eventAttachments_1 = tslib_1.__importDefault(require("app/components/events/eventAttachments"));
describe('EventAttachments', function () {
    var _a = initializeOrg_1.initializeOrg(), routerContext = _a.routerContext, organization = _a.organization, project = _a.project;
    // @ts-expect-error
    var event = TestStubs.Event({ metadata: { stripped_crash: true } });
    var props = {
        orgId: organization.slug,
        projectId: project.slug,
        location: routerContext.context.location,
        attachments: [],
        onDeleteAttachment: jest.fn(),
        event: event,
    };
    it('shows attachments limit reached notice', function () {
        var _a = reactTestingLibrary_1.mountWithTheme(<eventAttachments_1.default {...props}/>), getByText = _a.getByText, getByRole = _a.getByRole;
        expect(getByText('Attachments (0)')).toBeInTheDocument();
        expect(getByRole('link', { name: 'View crashes' })).toHaveAttribute('href', '');
        expect(getByRole('link', { name: 'configure limit' })).toHaveAttribute('href', "/settings/" + props.orgId + "/projects/" + props.projectId + "/security-and-privacy/");
        expect(getByText('Your limit of stored crash reports has been reached for this issue.')).toBeInTheDocument();
    });
    it('does not render anything if no attachments (nor stripped) are available', function () {
        var container = reactTestingLibrary_1.mountWithTheme(<eventAttachments_1.default {...props} event={tslib_1.__assign(tslib_1.__assign({}, event), { metadata: { stripped_crash: false } })}/>).container;
        expect(container).toBeEmptyDOMElement();
    });
});
//# sourceMappingURL=eventAttachments.spec.jsx.map