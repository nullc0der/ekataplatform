module.exports = [
	{
		name: 'Home',
		icon: 'fa fa-fw fa-home',
		href: '',
		children: [
			{
				name: 'Dashboard',
				href: '/dashboard/ ',
				external: true,
				icon: 'fa fa-fw fa-tachometer'
			},
			{
				name: 'My Accounts',
				href: '/myaccount/',
				external: true,
				icon: 'fa fa-fw fa-shield',
				//children: [
				//	{ name: 'Accounts', href: '/my-accounts/accounts', icon: 'fa fa-fw fa-circle-o'},
				//	{ name: 'Transfer', href: '/my-accounts/transfer', icon: 'fa fa-fw fa-circle-o'},
				//]
			},
			{ name: 'Profile', href: '/profile/', external: true, icon: 'fa fa-fw fa-circle-o'},
			{ name: 'Timeline', href: '/timeline/', external: true, icon: 'fa fa-fw fa-clock-o'},
			//{ name: 'Email', href: '/dashboard/', icon: 'fa fa-fw fa-envelope-o'},
			{ name: 'Messenger', href: '/messenger/', icon: 'fa fa-fw fa-comment-o'},
			//{ name: 'My Blog', href: '/dashboard/', icon: 'fa fa-fw fa-bookmark'}
		]
	},
	{
		name: 'Community',
		icon: 'fa fa-fw fa-compass',
		href: '',
		children: [
			//{ name: 'Home', icon: 'fa fa-fw fa-dashboard', href: '/community'},
			//{ name: "News", href: '', icon: 'fa fa-fw fa-shield'},
			//{ name: "Events", href: '', icon: 'fa fa-fw fa-calendar'},
			//{ name: "Bulletin Board", href: '', icon: 'fa fa-thumb-tack'},
			// {
			// 	name: "Groups",
			// 	href: '/community/groups',
			// 	icon: 'fa fa-fw fa-cubes'
			// },
			{
				name: "Members",
				href: '/members/',
				icon: 'fa fa-fw fa-users'
			},
			//{
			//	name: "Bloggers",
			//	href: '',
			//	icon: 'fa fa-fw fa-edit'
			//},
			//{
			//	name: "Administration",
			//	href: '',
			//	icon: 'fa fa-fw fa-university'
			//},
			//{
			//	name: "Market Place",
			//	href: '',
			//	icon: 'fa fa-fw fa-shopping-cart'
			//},
			//{
			//	name: "eBlast",
			//	href: '',
			//	icon: 'fa fa-fw fa-envelope',
			//	children: [
			//		{
			//			name: "Email Lists",
			//			href: "/eblast/emailgroups/",
			//			icon: "fa fa-fw fa-circle-o"
			//		},
			//		{
			//			name: "Email Templates",
			//			href: "/eblast/emailtemplates/",
			//			icon: "fa fa-fw fa-circle-o"
			//		},
			//		{
			//			name: "Email Campaigns",
			//			href: "/eblast/campaigns/",
			//			icon: "fa fa-fw fa-circle-o"
			//		},
			//	]
			//},
			//{
			//	name: "Subscriptions",
			//	href: '',
			//	icon: 'fa fa-fw fa-star'
			//},
		]
	},
]

let others = [
	{
		name: 'Applications',
		icon: 'fa fa-fw fa-futbol-o',
		href: '',
		children: [
			{
				name: "App Hastag Banner",
				icon: "fa fa-fw fa-dashboard",
				href: ''
			},
			{
				name: "Article Editor",
				icon: "fa fa-fw fa-pencil",
				href: ''
			},
			{
				name: "Messenger",
				icon: "fa fa-fw fa-comments",
				href: ''
			},
		]
	},
	{
		name: 'Groups',
		icon: 'fa fa-fw fa-cube',
		href: '',
		children: [
			{
				name: "Home",
				href: '',
				icon: 'fa fa-fw fa-home'
			},
			{
				name: "Dashboard",
				href: '',
				icon: 'fa fa-fw fa-dashboard'
			},
			{
				name: "Members",
				href: '/groups/members',
				icon: 'fa fa-fw fa-shield'
			},
			{
				name: "Profile",
				href: '',
				icon: 'fa fa-fw fa-user'
			},
			{
				name: "Timeline",
				href: '',
				icon: 'fa fa-fw fa-clock-o'
			},
			{
				name: "News",
				href: '',
				icon: 'fa fa-fw fa-user'
			},
			{
				name: "Events",
				href: '',
				icon: 'fa fa-fw fa-clock-o'
			},
			{
				name: "eBlast",
				href: '',
				icon: 'fa fa-fw fa-envelope',
				children: [
					{
						name: "Email Lists",
						href: "",
						icon: "fa fa-fw fa-circle-o"
					},
					{
						name: "Email Templates",
						href: "",
						icon: "fa fa-fw fa-circle-o"
					},
					{
						name: "Email Campaigns",
						href: "",
						icon: "fa fa-fw fa-circle-o"
					},
				]
			},
			{
				name: "Subscriptions",
				href: '',
				icon: 'fa fa-fw fa-star'
			},
		]
	},
	{
		name: 'Settings',
		icon: 'fa fa-fw fa-cog',
		href: '',
		children: [
			{
				name: "Account Settings",
				href: "",
				icon: "fa fa-fw fa-home"
			},
			{
				name: "Membership",
				href: "",
				icon: "fa fa-fw fa-dashboard"
			},
			{
				name: "Other",
				href: "",
				icon: "fa fa-fw fa-shield"
			},
		]
	}
]
