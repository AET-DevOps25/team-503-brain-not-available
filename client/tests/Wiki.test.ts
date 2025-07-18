vi.mock('../src/components/ui/sidebar/utils', async () => {
  const actual = await vi.importActual<any>('../src/components/ui/sidebar/utils')
  return {
    ...actual,
    useSidebar: () => ({
      isMobile: false,
      state: 'open',
      openMobile: false,
      setOpenMobile: vi.fn()
    })
  }
})

vi.mock('@/service/pageService', () => ({
  pageService: {
    getAllPages: vi.fn(),
    createPage: vi.fn(),
    deletePage: vi.fn()
  }
}))

import { describe, it, vi, beforeEach, expect } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AppSidebar from '../src/components/AppSidebar.vue'
import { pageService } from '../src/service/pageService'
import Button from '../src/components/ui/button/Button.vue'
import * as SidebarUI from '../src/components/ui/sidebar'
import * as DropdownMenu from '../src/components/ui/dropdown-menu'

// Use a wrapper to provide Sidebar context
const TestWrapper = {
  components: { AppSidebar, Sidebar: SidebarUI.Sidebar },
  template: `<Sidebar><AppSidebar /></Sidebar>`
}

function mountComponent() {
  return mount(TestWrapper, {
    global: {
      components: {
        Button,
        ...SidebarUI,
        ...DropdownMenu
      },
      stubs: {
        'router-link': {
          template: '<a><slot /></a>'
        }
      }
    }
  })
}

const mockPages = [
  { pageId: 1, title: 'Home' },
  { pageId: 2, title: 'About' },
]

describe('AppSidebar', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.stubGlobal('prompt', vi.fn())
    vi.stubGlobal('confirm', vi.fn())
  })

  it('loads pages on mount', async () => {
    (pageService.getAllPages as any).mockResolvedValue(mockPages)

    const wrapper = mountComponent()
    await flushPromises()

    expect(pageService.getAllPages).toHaveBeenCalled()
    expect(wrapper.text()).toContain('Home')
    expect(wrapper.text()).toContain('About')
  })

  it('creates a new page when prompt is accepted', async () => {
    (pageService.getAllPages as any).mockResolvedValue([])
    ;(pageService.createPage as any).mockResolvedValue({ pageId: 3, title: 'New Page' })
    ;(global.prompt as any).mockReturnValue('New Page')

    const wrapper = mountComponent()
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

    const wrapper = mountComponent()
    await flushPromises()

    // 1. find and click the "..." dropdown trigger
    const dropdownButtons = wrapper.findAll('button')
    const ellipsisButton = dropdownButtons.find(btn =>
        btn.attributes('title') === undefined && btn.html().includes('ellipsis')
    )

    expect(ellipsisButton).toBeDefined()
    await ellipsisButton!.trigger('click')
    await flushPromises()

    // 2. find the delete item and click it
    const deleteItem = wrapper.findAllComponents({ name: 'DropdownMenuItem' }).find(node =>
        node.text().includes('Löschen')
    )

    expect(deleteItem).toBeDefined()
    await deleteItem!.trigger('click')
    await flushPromises()

    expect(pageService.deletePage).toHaveBeenCalledWith(1)
    expect(wrapper.text()).not.toContain('Home')
  })

  it('does not create a page if prompt is empty', async () => {
    (pageService.getAllPages as any).mockResolvedValue([])
    ;(global.prompt as any).mockReturnValue('   ')

    const wrapper = mountComponent()
    await flushPromises()

    const button = wrapper.find('button[title="Neue Seite erstellen"]')
    await button.trigger('click')
    await flushPromises()

    expect(pageService.createPage).not.toHaveBeenCalled()
  })
})
