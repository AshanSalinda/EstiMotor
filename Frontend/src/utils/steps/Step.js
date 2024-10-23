
class Step {
    constructor(title, content) {
        this.title = title;
        this.content = content;
        this.isFailed = false;
        this.logs = [];
    }


    async start(log) {
        log(`${this.title} is starting...`, this.logs);
        // Simulate step completion with a timeout or actual logic here
        await new Promise(resolve => setTimeout(resolve, 2000)); 
        log(`${this.title} Completed...`, this.logs);
    }

    complete() {
        this.status = 'completed';
        this.logs.push(`Step "${this.label}" has completed successfully.`);
    }

    fail(reason) {
        this.status = 'failed';
        this.logs.push(`Step "${this.label}" failed: ${reason}`);
    }

    log(message) {
        this.logs.push(message);
    }
}

export default Step;
