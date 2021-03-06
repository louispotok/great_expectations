from collections import OrderedDict

from .renderer import Renderer
from great_expectations.render.types import (
    RenderedComponentContent,
    RenderedSectionContent,
    RenderedDocumentContent
)

# FIXME : This class needs to be rebuilt to accept SiteSectionIdentifiers as input.
# FIXME : This class needs tests.
class SiteIndexPageRenderer(Renderer):

    @classmethod
    def _generate_data_asset_table_section(cls, data_asset_name, link_lists_dict, link_list_keys_to_render):
        section_rows = []

        column_count = len(link_list_keys_to_render)
        profiling_links = link_lists_dict.get("profiling_links")
        validations_links = link_lists_dict.get("validations_links")
        expectations_links = link_lists_dict.get("expectations_links")
        
        cell_width_pct = 100.0/(column_count + 1)

        first_row = []
        rowspan = str(len(expectations_links)) if expectations_links else "1"
        
        data_asset_name = RenderedComponentContent(**{
            "content_block_type": "string_template",
            "string_template": {
                "template": "$data_asset",
                "params": {
                    "data_asset": data_asset_name
                },
                "tag": "blockquote",
                "styling": {
                    "params": {
                        "data_asset": {
                            "classes": ["blockquote"],
                        }
                    }
                }
            },
            "styling": {
                "classes": ["col-sm-3", "col-xs-12", "pl-sm-5", "pl-xs-0"],
                "styles": {
                    "margin-top": "10px",
                    "word-break": "break-all"
                },
                "parent": {
                    "styles": {
                        "width": "{}%".format(cell_width_pct)
                    },
                    "attributes": {
                        "rowspan": rowspan
                    }
                }
            }
        })
        first_row.append(data_asset_name)
        
        if "profiling_links" in link_list_keys_to_render:
            profiling_results_bullets = [
                RenderedComponentContent(**{
                    "content_block_type": "string_template",
                    "string_template": {
                        "template": "$link_text",
                        "params": {
                            "link_text": link_dict["expectation_suite_name"] + "-ProfilingResults"
                        },
                        "tag": "a",
                        "styling": {
                            "attributes": {
                                "href": link_dict["filepath"]
                            }
                        }
                    }
                }) for link_dict in profiling_links
            ]
            profiling_results_bullet_list = RenderedComponentContent(**{
                "content_block_type": "bullet_list",
                "bullet_list": profiling_results_bullets,
                "styling": {
                    "parent": {
                        "styles": {
                            "width": "{}%".format(cell_width_pct),
                        },
                        "attributes": {
                            "rowspan": rowspan
                        }
                    }
                }
            })
            first_row.append(profiling_results_bullet_list)
            
        if "expectations_links" in link_list_keys_to_render:
            if len(expectations_links) > 0:
                expectation_suite_link_dict = expectations_links[0]
            else:
                expectation_suite_link_dict = {
                    "expectation_suite_name": "",
                    "filepath": ""
                }

            expectation_suite_name = expectation_suite_link_dict["expectation_suite_name"]

            expectation_suite_link = RenderedComponentContent(**{
                "content_block_type": "string_template",
                "string_template": {
                    "template": "$link_text",
                    "params": {
                        "link_text": expectation_suite_name
                    },
                    "tag": "a",
                    "styling": {
                        "attributes": {
                            "href": expectation_suite_link_dict["filepath"]
                        },
                    }
                },
                "styling": {
                    "parent": {
                        "styles": {
                            "width": "{}%".format(cell_width_pct),
                        }
                    }
                }
            })
            first_row.append(expectation_suite_link)
            
            if "validations_links" in link_list_keys_to_render and "expectations_links" in link_list_keys_to_render:
                sorted_validations_links = [
                    link_dict for link_dict in sorted(validations_links, key=lambda x: x["run_id"], reverse=True)
                    if link_dict["expectation_suite_name"] == expectation_suite_name
                ]
                validation_link_bullets = [
                    RenderedComponentContent(**{
                        "content_block_type": "string_template",
                        "string_template": {
                            "template": "${validation_success} $link_text",
                            "params": {
                                "link_text": link_dict["run_id"],
                                "validation_success": ""
                            },
                            "tag": "a",
                            "styling": {
                                "attributes": {
                                    "href": link_dict["filepath"]
                                },
                                "params": {
                                    "validation_success": {
                                        "tag": "i",
                                        "classes": ["fas", "fa-check-circle", "text-success"] if link_dict[
                                            "validation_success"] else ["fas", "fa-times", "text-danger"]
                                    }
                                }
                            }
                        }
                    }) for link_dict in sorted_validations_links if
                    link_dict["expectation_suite_name"] == expectation_suite_name
                ]
                validation_link_bullet_list = RenderedComponentContent(**{
                    "content_block_type": "bullet_list",
                    "bullet_list": validation_link_bullets,
                    "styling": {
                        "parent": {
                            "styles": {
                                "width": "{}%".format(cell_width_pct)
                            }
                        },
                        "body": {
                            "styles": {
                                "max-height": "15em",
                                # "overflow": "scroll"
                            }
                        }
                    }
                })
                first_row.append(validation_link_bullet_list)

        if not expectations_links and "validations_links" in link_list_keys_to_render:
            sorted_validations_links = [
                link_dict for link_dict in sorted(validations_links, key=lambda x: x["run_id"], reverse=True)
            ]
            validation_link_bullets = [
                RenderedComponentContent(**{
                    "content_block_type": "string_template",
                    "string_template": {
                        "template": "${validation_success} $link_text",
                        "params": {
                            "link_text": link_dict["run_id"],
                            "validation_success": ""
                        },
                        "tag": "a",
                        "styling": {
                            "attributes": {
                                "href": link_dict["filepath"]
                            },
                            "params": {
                                "validation_success": {
                                    "tag": "i",
                                    "classes": ["fas", "fa-check-circle", "text-success"] if link_dict[
                                        "validation_success"] else ["fas", "fa-times", "text-danger"]
                                }
                            }
                        }
                    }
                }) for link_dict in sorted_validations_links
            ]
            validation_link_bullet_list = RenderedComponentContent(**{
                "content_block_type": "bullet_list",
                "bullet_list": validation_link_bullets,
                "styling": {
                    "parent": {
                        "styles": {
                            "width": "{}%".format(cell_width_pct)
                        }
                    },
                    "body": {
                        "styles": {
                            "max-height": "15em",
                            # "overflow": "scroll"
                        }
                    }
                }
            })
            first_row.append(validation_link_bullet_list)
        
        section_rows.append(first_row)
        
        if "expectations_links" in link_list_keys_to_render and len(expectations_links) > 1:
            for expectation_suite_link_dict in expectations_links[1:]:
                expectation_suite_row = []
                expectation_suite_name = expectation_suite_link_dict["expectation_suite_name"]
    
                expectation_suite_link = RenderedComponentContent(**{
                    "content_block_type": "string_template",
                    "string_template": {
                        "template": "$link_text",
                        "params": {
                            "link_text": expectation_suite_name
                        },
                        "tag": "a",
                        "styling": {
                            "attributes": {
                                "href": expectation_suite_link_dict["filepath"]
                            },
                        }
                    },
                    "styling": {
                        "parent": {
                            "styles": {
                                "width": "{}%".format(cell_width_pct),
                            }
                        }
                    }
                })
                expectation_suite_row.append(expectation_suite_link)
    
                if "validations_links" in link_list_keys_to_render:
                    sorted_validations_links = [
                        link_dict for link_dict in sorted(validations_links, key=lambda x: x["run_id"], reverse=True)
                        if link_dict["expectation_suite_name"] == expectation_suite_name
                    ]
                    validation_link_bullets = [
                        RenderedComponentContent(**{
                            "content_block_type": "string_template",
                            "string_template": {
                                "template": "${validation_success} $link_text",
                                "params": {
                                    "link_text": link_dict["run_id"],
                                    "validation_success": ""
                                },
                                "tag": "a",
                                "styling": {
                                    "attributes": {
                                        "href": link_dict["filepath"]
                                    },
                                    "params": {
                                        "validation_success": {
                                            "tag": "i",
                                            "classes": ["fas", "fa-check-circle",  "text-success"] if link_dict["validation_success"] else ["fas", "fa-times", "text-danger"]
                                        }
                                    }
                                }
                            }
                        }) for link_dict in sorted_validations_links if
                        link_dict["expectation_suite_name"] == expectation_suite_name
                    ]
                    validation_link_bullet_list = RenderedComponentContent(**{
                        "content_block_type": "bullet_list",
                        "bullet_list": validation_link_bullets,
                        "styling": {
                            "parent": {
                                "styles": {
                                    "width": "{}%".format(cell_width_pct)
                                }
                            },
                            "body": {
                                "styles": {
                                    "max-height": "15em",
                                    # "overflow": "scroll"
                                }
                            }
                        }
                    })
                    expectation_suite_row.append(validation_link_bullet_list)
                    
                section_rows.append(expectation_suite_row)
            
        return section_rows
        
    @classmethod
    def render(cls, index_links_dict):

        sections = []

        for source, generators in index_links_dict.items():
            content_blocks = []

            # datasource header
            source_header_block = RenderedComponentContent(**{
                "content_block_type": "header",
                "header": source,
                "styling": {
                    "classes": ["col-12"],
                    "header": {
                        "classes": ["alert", "alert-secondary"]
                    }
                }
            })
            content_blocks.append(source_header_block)

            # generator header
            for generator, data_assets in generators.items():
                generator_header_block = RenderedComponentContent(**{
                    "content_block_type": "header",
                    "header": generator,
                    "styling": {
                        "classes": ["col-12", "ml-4"],
                    }
                })
                content_blocks.append(generator_header_block)

                horizontal_rule = RenderedComponentContent(**{
                    "content_block_type": "string_template",
                    "string_template": {
                        "template": "",
                        "params": {},
                        "tag": "hr"
                    },
                    "styling": {
                        "classes": ["col-12"],
                    }
                })
                content_blocks.append(horizontal_rule)

                generator_table_rows = []
                generator_table_header_row = ["Data Asset"]
                link_list_keys_to_render = []
                
                header_dict = OrderedDict([
                    ["profiling_links", "Profiling Results"],
                    ["expectations_links", "Expectation Suite"],
                    ["validations_links", "Validation Results"]
                ])
                
                for link_lists_key, header in header_dict.items():
                    for data_asset, link_lists in data_assets.items():
                        if header in generator_table_header_row:
                            continue
                        if link_lists.get(link_lists_key):
                            generator_table_header_row.append(header)
                            link_list_keys_to_render.append(link_lists_key)
                
                generator_table = RenderedComponentContent(**{
                    "content_block_type": "table",
                    "header_row": generator_table_header_row,
                    "table": generator_table_rows,
                    "styling": {
                        "classes": ["col-12"],
                        "styles": {
                            "margin-top": "10px"
                        },
                        "body": {
                            "classes": ["table", "table-sm"]
                        }
                    }
                })
                # data_assets
                for data_asset, link_lists in data_assets.items():
                    generator_table_rows += cls._generate_data_asset_table_section(data_asset, link_lists, link_list_keys_to_render=link_list_keys_to_render)
                    
                content_blocks.append(generator_table)

            section = RenderedSectionContent(**{
                "section_name": source,
                "content_blocks": content_blocks
            })
            sections.append(section)

        return RenderedDocumentContent(**{
                "utm_medium": "index-page",
                "sections": sections
            })
