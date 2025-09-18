import { DocumentEdit20Regular, Person20Regular, Phone20Regular, ShoppingBag20Regular, DocumentHeart20Regular } from "@fluentui/react-icons";

export interface QuickTask {
    id: string;
    title: string;
    description: string;
    icon: React.ReactNode;
}

export const quickTasks: QuickTask[] = [
    {
        id: "onboard",
        title: "Heart History",
        description: "Based on the Henderson patient history, summarize key health events, with relevance for cardiac radiology.",
        icon: <Person20Regular />,
    },
    {
        id: "mobile",
        title: "Lungs History",
        description: "Based on the Linda Marie Williams patient history, summarize key health events, with relevance for lungs radiology.",
        icon: <Phone20Regular />,
    },
    {
        id: "fhir-summary",
        title: "Patient Summary",
        description: "Generate a concise medical history summary for patient-p01 including major diagnoses, lab tests, and medications.",
        icon: <DocumentHeart20Regular />,
    },
    // {
    //     id: "addon",
    //     title: "Buy add-on",
    //     description: "Enable roaming on mobile plan, starting next week.",
    //     icon: <ShoppingBag20Regular />,
    // },
    // {
    //     id: "press",
    //     title: "Draft a press release",
    //     description: "Write a press release about our current products.",
    //     icon: <DocumentEdit20Regular />,
    // },
];

export interface HomeInputProps {
    onInputSubmit: (input: string) => void;
    onQuickTaskSelect: (taskDescription: string) => void;
}
