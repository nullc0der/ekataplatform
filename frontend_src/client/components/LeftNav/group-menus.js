const groupMenus = (permissions, id) => {
    let menu = {
        name: 'Groups',
        icon: 'fa fa-fw fa-cube',
        href: '',
        children: [
        ]
    }
    if (permissions.indexOf(102) !== -1) {
        menu = {
            ...menu, children: [...menu.children,
                {
                  name: "Posts",
                  href: `/community/1/groups/${id}/posts`,
                  icon: 'fa fa-fw fa-life-ring'
              },
              {
                name: "Members",
                href: `/community/1/groups/${id}/members`,
                icon: 'fa fa-fw fa-shield',
                children: [
                    (permissions.indexOf(103) !== -1 || permissions.indexOf(104) !== -1) &&
                    {
                        name: "Management",
                        href: `/community/1/groups/${id}/members/management`,
                        icon: 'fa fa-fw fa-users'
                    }
                ]
            }
          ]
        }
    }
    if (permissions.indexOf(103) !== -1 || permissions.indexOf(104) !== -1) {
        menu = {
            ...menu, children: [...menu.children, {
                name: "Profile",
                href: `/community/1/groups/${id}/profile`,
                icon: 'fa fa-fw fa-gear'
            }]
        }
    }
    if (menu.children.length === 0) {
        menu = {}
    }
    return (
        menu
    )
}

export default groupMenus
