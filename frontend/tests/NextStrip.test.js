// MyComponent.test.js
import { defineComponent } from 'vue'
import { mount, flushPromises, RouterLinkStub } from '@vue/test-utils'
import NextStrip from '../src/components/NextStrip.vue'
import StripMethodsAPI from '../src/api/resources/StripMethods'

const mockNextStripData = {
    datetime: "2023-01-01T12:00:00",
    section: "Section 4",
    setters: "fribyg"
}

test('next strip', async () => {
    // first some sanity checks if component exists and api resource exists
    expect(NextStrip).toBeTruthy();
    expect(StripMethodsAPI).toBeTruthy();

    // must wrap the component in a suspense as it uses async setup
    const TestComponent = defineComponent({
        components: { NextStrip },
        template: '<Suspense><NextStrip/></Suspense>'
    })

    // mock the api method
    const spy = vi.spyOn(StripMethodsAPI, 'index').mockResolvedValue(mockNextStripData)

    // add the routerlinkstub
    const wrapper = mount(TestComponent, {
        global: {
            stubs: {
                RouterLink: RouterLinkStub,
            },
        }
    })

    expect(StripMethodsAPI.index).toHaveBeenCalledTimes(1)

    // Wait until the DOM updates.
    await flushPromises()

    const header = wrapper.get("h2")
    // should match the mocked strip data
    expect(header.text()).toEqual('Section 4 strip 1 Jan')
})