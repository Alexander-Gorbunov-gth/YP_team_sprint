
export class AppError extends Error {
  constructor({ code = "UNKNOWN", message = "Произошла ошибка", details = null, status = 0 }) {
    super(message);
    this.name = "AppError";
    this.code = code;
    this.details = details;
    this.status = status;
  }
}