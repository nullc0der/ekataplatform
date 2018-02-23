const groupMenus = (permissions, id) => {
    let menu = {
        name: 'Groups',
        icon: 'fa fa-fw fa-cube',
        href: '',
        children: [
        ]
    }
    if (permissions.indexOf(103) !== -1 || permissions.indexOf(104) !== -1) {
        menu = {
            ...menu, children: [...menu.children, {
                name: "Members",
                href: '',
                icon: 'fa fa-fw fa-shield',
                children: [
                    {
                        name: "Management",
                        href: `/community/1/groups/${id}/members/management`,
                        icon: 'fa fa-fw fa-users'
                    }
                ]
            },
            {
                name: "Settings",
                href: `/community/1/groups/${id}/settings`,
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
