import {generateRandomDate} from 'utils/common'

var messages = [
	{
		from: 'username1',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'me',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'username1',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'me',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'username1',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'username1',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'me',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'username1',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'username1',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	},{
		from: 'me',
		from_user_id: 'xx1912992',
		message: 'Lorem ipsum solor di amet'
	}
]


messages = messages.map((x,i)=> {
	return {
		...x,
		stamp: generateRandomDate()
	}
})

export default messages

