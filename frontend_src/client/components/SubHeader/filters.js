module.exports = {
    "members": {
        enabledFilters: ['online', 'offline', 'staff', 'member'],
        disabledFilters: []
    },
    "community/groups": {
        enabledFilters: ['all', 'subscribed', 'joined'],
        disabledFilters: []
    },
    "community/groups/members": {
        enabledFilters: [
            'owners',
            'admins',
            'moderators',
            'staffs',
            'members'
        ],
        disabledFilters: [
            'online',
            'Ekata Members'
        ]
    },
    "community/groups/members/management": {
        enabledFilters: [
            'owners',
            'admins',
            'moderators',
            'staffs',
            'members',
            'subscribers'
        ],
        disabledFilters: [
            'online',
            'banned',
            'blocked'
        ]
    }
}
