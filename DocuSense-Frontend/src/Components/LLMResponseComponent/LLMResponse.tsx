import {
    codeBlockLookBack,
    findCompleteCodeBlock,
    findPartialCodeBlock,
} from "@llm-ui/code";
import { useLLMOutput } from "@llm-ui/react";
import { markdownLookBack } from "@llm-ui/markdown";
import React, {useEffect, useState} from "react";
import MarkdownComponent from "./MarkdownComponent.tsx";
import CodeBlock from "./CodeBlock.tsx";
import {CHAT_ENDPOINT} from "../Constants/APIConstants.ts";

export interface LLMResponseProps {
    chat_message: string;
    chat_name: string;
    set_sending: React.Dispatch<boolean>
}

interface ChunkTextResponse {
    text: string;
}

const LLMResponse =
    ( {chat_message, chat_name, set_sending}: LLMResponseProps ) => {

    const [output, setOutput] = useState<string>("");
    const [errorMessage, setErrorMessage] = useState<string>("");
    const [_, setIsStarted] = useState(false);
    const [isStreamFinished, setIsStreamFinished] = useState<boolean>(false);

    useEffect(() => {

        setIsStarted(true);
        setOutput("");

        const params = new URLSearchParams({
           chat_message: chat_message,
           chat_name: chat_name,
        });
        const eventSource = new EventSource(CHAT_ENDPOINT + "?" + params.toString());

        // Error occurred:
        eventSource.addEventListener("error", (e) => {
            console.log(e)
            setErrorMessage("An error occurred while generating this response.");
            eventSource.close();
            set_sending(false);
        });

        // When a new text chunk arrives:
        eventSource.addEventListener("chunk", (e) => {
            const token = JSON.parse(e.data) as ChunkTextResponse;
            setOutput((prevResponse) => `${prevResponse}${token.text}`);
        });

        // Once the finish event comes:
        eventSource.addEventListener("finish", () => {
            console.log("Finished.");

            set_sending(false);

            eventSource.close();
            setIsStreamFinished(true);
        });

        // Component unload, close the event listener:
        return () => eventSource.close();

    }, []);
    // const startChat = useCallback(() => {
    //
    //     setIsStarted(true);
    //     setOutput("");
    //
    //     const eventSource = new EventSource(CHAT_ENDPOINT + `?chat_message=${chat_message}&chat_name=${chat_name}`);
    //
    //     // Error occurred:
    //     eventSource.addEventListener("error", () => {
    //         setErrorMessage("An error occurred while generating this response.");
    //         eventSource.close();
    //     });
    //
    //     // When a new text chunk arrives:
    //     eventSource.addEventListener("chunk", (e) => {
    //         const token = JSON.parse(e.data) as ChunkTextResponse;
    //         setOutput((prevResponse) => `${prevResponse}${token.text}`);
    //     });
    //
    //     // Once the finish event comes:
    //     eventSource.addEventListener("finish", () => {
    //         eventSource.close();
    //         setIsStreamFinished(true);
    //     });
    //
    //     // Component unload, close the event listener:
    //     return () => eventSource.close();
    //
    // }, []);

    const { blockMatches } = useLLMOutput({
        llmOutput: output,
        fallbackBlock: {
            component: MarkdownComponent,
            lookBack: markdownLookBack(),
        },
        blocks: [
            {
                component: CodeBlock,
                findCompleteMatch: findCompleteCodeBlock(),
                findPartialMatch: findPartialCodeBlock(),
                lookBack: codeBlockLookBack(),
            },
        ],
        isStreamFinished,
    });

    return (
        <div>
            {/*{!isStarted && <button onClick={startChat}>Start</button>}*/}
            {blockMatches.map((blockMatch, index) => {
                const Component = blockMatch.block.component;
                return <Component key={index} blockMatch={blockMatch}/>;
            })}
            {
                errorMessage.length > 0 &&
                <>
                    <hr />
                    {errorMessage}
                </>
            }
        </div>
    );
}

export default LLMResponse;