import { describe, it, vi, beforeEach, expect } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AppSidebar from '../src/components/AppSidebar.vue'
import * as SidebarUI from '../src/components/ui/sidebar'
import * as DropdownMenu from '../src/components/ui/dropdown-menu'
import Button from '../src/components/ui/button/Button.vue'
import { pageService } from '../src/service/pageService'

vi.mock('@/service/pageService', () => ({
  pageService: {
    getAllPages: vi.fn(),
    createPage: vi.fn(),
    deletePage: vi.fn()
  }
}))

// Mock data
const mockPages = [
  { pageId: 1, title: 'Home' },
  { pageId: 2, title: 'About' },
]

function mountComponent() {
  return mount(AppSidebar, {
    global: {
      components: {
        Button,
        ...SidebarUI,
        ...DropdownMenu,
      },
      stubs: {
        'router-link': {
          template: '<a><slot /></a>'
        }
      }
    }
  })
}

describe('AppSidebar', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.stubGlobal('prompt', vi.fn())
    vi.stubGlobal('confirm', vi.fn())
  })

  it('loads pages on mount', async () => {
    (pageService.getAllPages as any).mockResolvedValue(mockPages)

    const wrapper = mount(AppSidebar)
    await flushPromises()

    expect(pageService.getAllPages).toHaveBeenCalled()
    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('About')
  })

  it('creates a new page when prompt is accepted', async () => {
    (pageService.getAllPages as any).mockResolvedValue([])
    ;(pageService.createPage as any).mockResolvedValue({ pageId: 3, title: 'New Page' })
    ;(global.prompt as any).mockReturnValue('New Page')

    const wrapper = mount(AppSidebar)
    await flushPromises()

    const button = wrapper.find('button[title="Neue Seite erstellen"]')
    await button.trigger('click')
    await flushPromises()

    expect(pageService.createPage).toHaveBeenCalledWith({ title: 'New Page', content: '' })
    expect(wrapper.text()).toContain('New Page')
  })

  it('deletes a page when confirmed', async () => {
    (pageService.getAllPages as any).mockResolvedValue(mockPages)
    ;(pageService.deletePage as any).mockResolvedValue()
    ;(global.confirm as any).mockReturnValue(true)

    const wrapper = mount(AppSidebar)
    await flushPromises()

    const deleteButtons = wrapper.findAllComponents({ name: 'DropdownMenuItem' })
    await deleteButtons[0].trigger('click') // Click "Löschen" for first page
    await flushPromises()

    expect(pageService.deletePage).toHaveBeenCalledWith(1)
    expect(wrapper.text()).not.toContain('Home')
  })

  it('does not create a page if prompt is empty', async () => {
    (pageService.getAllPages as any).mockResolvedValue([])
    ;(global.prompt as any).mockReturnValue('   ') // spaces only

    const wrapper = mount(AppSidebar)
    await flushPromises()

    const button = wrapper.find('button[title="Neue Seite erstellen"]')
    await button.trigger('click')
    await flushPromises()

    expect(pageService.createPage).not.toHaveBeenCalled()
  })
})
