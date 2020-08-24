const OneK = 1000;
const OneL = 100000;
const OneCr= 10000000;

const RUPEE_SYMBOL = '₹';

export function toDigits(num){
	const n = num.toString().replace(/\D/g, '')
	return parseInt(n, 10)
}

export function toFixed(num, prec = 2){
	num = Number.isFinite(num) ? num : 0;
	return parseFloat(num.toFixed(prec), 10);
}

export function numberToK(num, clamp = false){
	return `${clamp ? Math.floor(num/OneK) : toFixed(num/OneK)}K`
}

export function numberToL(num, clamp = false){
	return `${clamp ? Math.floor(num/OneL) : toFixed(num/OneL)}L`
}

export function numberToCr(num, clamp = false){
	return `${clamp ? Math.floor(num/OneCr) : toFixed(num/OneCr)}Cr`
}

export function toRupees(num){
	if (Number.isNaN(num) || !Number.isFinite(num)){
		return false
	}
	return num.toLocaleString('en-IN')
}

export function toRupeeStr(str){
	let result = 0;
	let input;
	if (typeof str !== "string")
		return `${RUPEE_SYMBOL} ${toRupees(str)}`
	
	input = str.replace(/\D/g, '')
	if (!input.length)
		return `${RUPEE_SYMBOL} ${toRupees(0)}`
	return `${RUPEE_SYMBOL} ${toRupees(Number(input))}`
}

export function toHumanNumber(num, clamp = false){
	return (
		num >= OneCr
			? numberToCr(num, clamp)
			: num >= OneL
				? numberToL(num, clamp)
				: num >= OneK
					? numberToK(num, clamp)
					: num
	)
}


export function toHumanRupees(num){
	return `${RUPEE_SYMBOL}${toHumanNumber(num)}`
}