# Numbers and Operations
# Author: Ubial
# 5 November 2025

# Create an algorithm to gather
# data to find the most popular
# bubble tea place around us

# Version 1
def vote_listed_choices():
    """Display all voting choices
    5 users vote for their choice
    Results will be printed"""
    CHOICES = ["A. CoCo", "B. Chatime", "C. BUBBLE WAFFEL", "D. gong cha"]

    # Buckets to hold all the votes
    coco = 0
    chatime = 0
    bubble_waffel = 0
    gong_cha = 0
    spoiled_votes = 0

    # Show all the bbt choices
    print("Vote for your favourite from the list.")
    print("Give the letter of your choice.")
    for choice in CHOICES:
        print(choice)
    # Ask the user for their choice
    vote = input("Your vote: ").lower().strip(",.?! ")
    # Add their vote to a running
    # tally
    if vote == "a":
        coco = coco + 1  # incrementation
    elif vote == "b":
        chatime += 1
    elif vote == "c":
        bubble_waffel += 1
    elif vote == "d":
        gong_cha += 1
    else:
        spoiled_votes += 1
    # Give some raw scores
    # Show the scores of coco, ..., etc.
    print(f"CoCo votes: {coco}")
    print(f"Chatime votes: {chatime}")
    print(f"BUBBLE WAFFEL votes: {bubble_waffel}")
    print(f"Gong Cha votes: {gong_cha}")
    print(f"Spoiled votes: {spoiled_votes}")
    # Give score as a percentage
    coco_percentage = coco / (coco + chatime + bubble_waffel + gong_cha + spoiled_votes)
    print(f"CoCo Percentage: {coco_percentage * 100}%")
    chatime_percentage = chatime / (
        coco + chatime + bubble_waffel + gong_cha + spoiled_votes
    )
    print(f"Chatime Percentage: {chatime_percentage * 100}%")
    bubble_waffel_percentage = bubble_waffel / (
        coco + chatime + bubble_waffel + gong_cha + spoiled_votes
    )
    print(f"Bubble Waffel Percentage: {bubble_waffel_percentage * 100}%")
    gong_cha_percentage = gong_cha / (
        coco + chatime + bubble_waffel + gong_cha + spoiled_votes
    )
    print(f"Gong Cha Percentage: {gong_cha_percentage * 100}%")


# Version 2
# Ask the user what their fave
# bbt place is
# Add their vote to a running
# tally
# Give the raw score
# Give score as percentage


def main():
    vote_listed_choices()


if __name__ == "__main__":
    main()
