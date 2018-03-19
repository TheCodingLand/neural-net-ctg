interface sessioninfo {
    userName: string;
    model: string;
    words: [ word ],
    brain: [ brainitem ], 
    conversationHistory: [ chatline]       

}


interface word { id : number, word: string, confidence: number }

interface brainitem { id : number, category:string , confidence: number }

interface chatline { id:number, user: string, content:string}
