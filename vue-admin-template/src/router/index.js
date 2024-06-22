import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  }

  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/table',
  //   name: 'Example',
  //   meta: { title: 'Example', icon: 'el-icon-s-help' },
  //   children: [
  //     {
  //       path: 'table',
  //       name: 'Table',
  //       component: () => import('@/views/table/index'),
  //       meta: { title: 'Table', icon: 'table' }
  //     },
  //     {
  //       path: 'tree',
  //       name: 'Tree',
  //       component: () => import('@/views/tree/index'),
  //       meta: { title: 'Tree', icon: 'tree' }
  //     }
  //   ]
  // },

  // {
  //   path: '/form',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'Form',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: 'Form', icon: 'form' }
  //     }
  //   ]
  // }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  // {
  //   path: '/nested',
  //   component: Layout,
  //   redirect: '/nested/menu1',
  //   name: 'Nested',
  //   meta: {
  //     title: 'Nested',
  //     icon: 'nested'
  //   },
  //   children: [
  //     {
  //       path: 'menu1',
  //       component: () => import('@/views/nested/menu1/index'), // Parent router-view
  //       name: 'Menu1',
  //       meta: { title: 'Menu1' },
  //       children: [
  //         {
  //           path: 'menu1-1',
  //           component: () => import('@/views/nested/menu1/menu1-1'),
  //           name: 'Menu1-1',
  //           meta: { title: 'Menu1-1' }
  //         },
  //         {
  //           path: 'menu1-2',
  //           component: () => import('@/views/nested/menu1/menu1-2'),
  //           name: 'Menu1-2',
  //           meta: { title: 'Menu1-2' },
  //           children: [
  //             {
  //               path: 'menu1-2-1',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
  //               name: 'Menu1-2-1',
  //               meta: { title: 'Menu1-2-1' }
  //             },
  //             {
  //               path: 'menu1-2-2',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
  //               name: 'Menu1-2-2',
  //               meta: { title: 'Menu1-2-2' }
  //             }
  //           ]
  //         },
  //         {
  //           path: 'menu1-3',
  //           component: () => import('@/views/nested/menu1/menu1-3'),
  //           name: 'Menu1-3',
  //           meta: { title: 'Menu1-3' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'menu2',
  //       component: () => import('@/views/nested/menu2/index'),
  //       meta: { title: 'menu2' }
  //     }
  //   ]
  // },

  {
    path: '/search-book',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'SearchBook',
        component: () => import('@/views/book_search/index'),
        meta: {
          title: '图书检索',
          icon: 'el-icon-search',
          roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin']
        }
      }
    ]
  },

  {
    path: '/manage-book',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'ManageBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'ManageBook',

        component: () => import('@/views/book/index'),
        meta: {
          title: '图书管理',
          icon: 'el-icon-s-help',
          roles: ['Librarian', 'LibraryDirector', 'admin']
        }
      }
    ]
  },

  {
    path: '/borrow/info',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'BorrowInfo',
        component: () => import('@/views/borrow/borrow_info.vue'),
        meta: {
          title: '借阅管理',
          icon: 'form',
          roles: ['Librarian', 'LibraryDirector', 'admin']
        }
      }
    ]
  },

  {
    path: '/reservation/info',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'ReservationInfo',
        component: () => import('@/views/reserve/reservation_info.vue'),
        meta: {
          title: '预约管理',
          icon: 'guide',
          roles: ['Librarian', 'LibraryDirector', 'admin']
        }
      }
    ]
  },

  {
    path: '/late-fee/info',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'LateFeeInfo',
        component: () => import('@/views/late_fine/late_fine_info.vue'),
        meta: {
          title: '违期管理',
          icon: 'edit',
          roles: ['Librarian', 'LibraryDirector', 'admin']
        }
      }
    ]
  },

  {
    path: '/reader/manage',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'ReaderManage',
        component: () => import('@/views/reader/reader_info.vue'),
        meta: {
          title: '读者管理',
          icon: 'peoples',
          roles: ['Librarian', 'LibraryDirector', 'admin']
        }
      }
    ]
  },

  {
    path: '/borrow/reader',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'ReaderBorrowInfo',
        component: () => import('@/views/borrow/reader_borrow.vue'),
        meta: {
          title: '个人借阅信息',
          icon: 'list',
          roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin']
        }
      }
    ]
  },

  {
    path: '/reservation/reader',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'ReaderReservationInfo',
        component: () => import('@/views/reserve/reader_reservation.vue'),
        meta: {
          title: '个人预约信息',
          icon: 'tab',
          roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin']
        }
      }
    ]
  },

  {
    path: '/late-fee/reader',
    component: Layout,
    // redirect: '/book/search-book',
    // name: 'SearchBook',
    meta: { roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin'] },
    children: [
      {
        path: 'index',
        name: 'ReaderLateFeeInfo',
        component: () => import('@/views/late_fine/reader_late_fine_info.vue'),
        meta: {
          title: '个人违期信息',
          icon: 'lock',
          roles: ['Librarian', 'LibraryDirector', 'Reader', 'admin']
        }
      }
    ]
  },

  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
        meta: { title: 'External Link', icon: 'link' }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
