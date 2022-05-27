
const splitArrayInX = (arr_, X) => {
  let res = []
  for (let i = 0; i < arr_.length; i += X) {
    res.push(arr_.slice(i, i + X));
  }
  return res
};

export default splitArrayInX;
