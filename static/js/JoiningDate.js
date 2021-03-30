let joining = document.getElementById("joining");
let joiningDate = new Date(joining.innerHTML).getTime();
let today = new Date().getTime();

let diff = today - joiningDate;
days = Math.floor(diff / (1000 * 60 * 60 * 24));
hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

let message = "";
if (days >= 365) {
message = `${Math.floor(Number(days) / 365)}y`;
} else if (days >= 30) {
message = `${Math.floor(Number(days) / 30)}M`;
} else if (days <= 0) {
if (hours <= 0) {
message = `${mins}m`;
} else {
message = `${hours}h`;
}
} else {
message = `${days}d`;
}
joining.innerHTML = `Joined ${message} ago`;
