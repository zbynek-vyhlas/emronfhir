function getInitials(firstName, lastName) {
  let firtsLetter = firstName ? firstName.charAt(0).toUpperCase() : "";
  let secondLetter = lastName ? lastName.charAt(0).toUpperCase() : "";
  return firtsLetter + secondLetter;
}

function getUserType(user) {
  return user.isSuperuser ? "superuser" : user.isStaff ? "staff" : null;
}

export { getInitials, getUserType };
